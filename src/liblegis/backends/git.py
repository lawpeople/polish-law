import pathlib
import re
from typing import TypedDict

from pygit2 import Repository

from liblegis.backends.base import Backend, LegalAct


class JournalIndexConfig(TypedDict):
    commit_id: str
    is_deleted: bool
    journal_volume: int


JOURNAL_LINE_PATTERN = re.compile(
    r"Dz.U. (?P<year>(\d{4})) nr (?P<volume>(\d+)) poz. (?P<position>(\d+))"
)


class LocalGitBackend(Backend):
    def __init__(self) -> None:
        self._cursor = None
        self._repo = Repository("data/.git")
        self._journal_index: list[tuple[int, int]] = []
        self._journal_metadata: dict[tuple[int, int], JournalIndexConfig] = {}
        self._build_journal_index_and_metadata()

    def _build_journal_index_and_metadata(self):
        for commit in self._repo.walk(self._repo.head.target):
            journal_line = commit.message.splitlines()[0]
            journal_data = self._get_journal_data_from_line(journal_line)

            index_entry = (journal_data["year"], journal_data["position"])
            self._journal_index.append(index_entry)
            self._journal_metadata[index_entry] = {
                "commit_id": commit.short_id,
                "is_deleted": False,
                "journal_volume": journal_data["volume"],
            }

        self._journal_index.sort()

    def _get_journal_data_from_line(self, journal_line: str) -> dict[str, int]:
        result = JOURNAL_LINE_PATTERN.match(journal_line)
        if not result:
            raise RuntimeError()

        return {k: int(v) for k, v in result.groupdict().items()}

    def _get_legal_act(self, year: int, position: int) -> LegalAct:
        commit_message = self._get_commit_message(year, position)
        act_content = self._get_content(year, position)

        journal_info, _, act_title, *meta_info = commit_message.splitlines()
        volume = int(journal_info.split()[3])
        return LegalAct(year, volume, position, act_title, act_content)

    def _get_commit_message(self, year: int, position: int) -> str:
        index_key = (year, position)
        if index_key in self._journal_metadata:
            commit_id = self._journal_metadata[index_key]["commit_id"]
            return self._repo.revparse_single(commit_id).message

        raise RuntimeError()

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
