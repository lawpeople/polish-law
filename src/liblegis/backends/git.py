import pathlib
import re
from typing import TypedDict

from pygit2 import GIT_SORT_REVERSE, Repository

from liblegis.backends.base import Backend, LegalAct


class JournalIndexConfig(TypedDict):
    commit_id: str
    is_deleted: bool
    journal_volume: int


JOURNAL_LINE_PATTERN = re.compile(
    r"Dz.U. (?P<year>(\d{4})) nr (?P<volume>(\d+)) poz. (?P<position>(\d+))"
)

IS_DELETED_FIELDS = {"Akty uchylone", "Akty uznane za uchylone"}


class LocalGitBackend(Backend):
    def __init__(self) -> None:
        self._cursor = None
        self._repo = Repository("data/.git")
        self._journal_index: list[tuple[int, int]] = []
        self._journal_metadata: dict[tuple[int, int], JournalIndexConfig] = {}
        self._build_journal_index_and_metadata()

    def _build_journal_index_and_metadata(self):
        for commit in self._repo.walk(self._repo.head.target, GIT_SORT_REVERSE):
            journal_line = commit.message.splitlines()[0]
            journal_data = self._get_journal_data_from_line(journal_line)

            index_key = (journal_data["year"], journal_data["position"])
            self._journal_index.append(index_key)
            self._journal_metadata[index_key] = {
                "commit_id": commit.short_id,
                "is_deleted": False,
                "journal_volume": journal_data["volume"],
            }

            deleted_journal_entries = self._get_deleted_journal_entries(commit.message)
            for entry in deleted_journal_entries:
                self._journal_metadata[entry]["is_deleted"] = True

        self._journal_index.sort()

    def _get_deleted_journal_entries(
        self, commit_message: str
    ) -> list[tuple[int, int]]:
        for line in commit_message.splitlines()[4:]:
            field, value = line.split(": ")
            if field in IS_DELETED_FIELDS:
                journal_entries: list[tuple[int, int]] = []
                journal_lines = value.split("; ")
                for line in journal_lines:
                    journal_data = self._get_journal_data_from_line(line)
                    journal_entries.append(
                        (journal_data["year"], journal_data["position"])
                    )
                return journal_entries
        return []

    def _get_journal_data_from_line(self, journal_line: str) -> dict[str, int]:
        result = JOURNAL_LINE_PATTERN.match(journal_line)
        if not result:
            raise RuntimeError()

        return {k: int(v) for k, v in result.groupdict().items()}

    def _get_legal_act(self, year: int, position: int) -> LegalAct:
        index_key = (year, position)
        if index_key not in self._journal_metadata:
            raise RuntimeError()

        commit_message = self._get_commit_message(index_key)
        if not self._is_deleted(index_key):
            act_content = self._get_content(year, position)
        else:
            act_content = None

        journal_info, _, act_title, *_ = commit_message.splitlines()
        volume = int(journal_info.split()[3])
        return LegalAct(year, volume, position, act_title, act_content)

    def _is_deleted(self, index_key: tuple[int, int]) -> bool:
        return self._journal_metadata[index_key]["is_deleted"] is True

    def _get_commit_message(self, index_key: tuple[int, int]) -> str:
        # TODO: Remove this method and put data into journal_metadata
        commit_id = self._journal_metadata[index_key]["commit_id"]
        return self._repo.revparse_single(commit_id).message

    def _get_content(self, year: int, position: int) -> str:
        searched_filename = f"D{year}{position:>04}.md"

        data_path_glob = pathlib.Path("./data").glob("**/*.md")
        for filepath in data_path_glob:
            if filepath.name == searched_filename:
                with open(filepath) as f:
                    return f.read()

        raise RuntimeError()

    def _get_next_legal_act_index(self) -> tuple[int, int] | None:
        if self._cursor is None:
            raise RuntimeError()
        inext = self._journal_index.index(self._cursor) + 1
        return self._journal_index[inext] if inext < len(self._journal_index) else None
