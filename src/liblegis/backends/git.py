import pathlib
import re
from typing import TypedDict

from pygit2 import GIT_SORT_REVERSE, Commit, Repository

from liblegis.backends.base import Backend, LegalAct


class JournalIndexConfig(TypedDict):
    title: str
    commit_id: str
    is_deleted: bool
    journal_volume: int
    promulgation_date: str | None
    announcement_date: str | None
    comes_in_force_date: str | None
    effective_date: str | None


JOURNAL_LINE_PATTERN = re.compile(
    r"Dz.U. (?P<year>(\d{4})) nr (?P<volume>(\d+)) poz. (?P<position>(\d+))"
)


class Metadata:
    _FIELDS_MAP = {
        "promulgation_date": "Data ogłoszenia",
        "announcement_date": "Data wydania",
        "comes_in_force_date": "Data wejścia w życie",
        "effective_date": "Data obowiązywania",
    }
    _IS_DELETED_FIELDS = {"Akty uchylone", "Akty uznane za uchylone"}

    def __init__(self, commit: Commit) -> None:
        self._commit = commit
        self._data = dict(
            [line.split(": ") for line in commit.message.splitlines()[3:]]
        )

    @property
    def journal_data(self) -> dict[str, int]:
        return self._get_journal_data_from_line(self._commit.message.splitlines()[0])

    @property
    def title(self) -> str:
        return self._commit.message.splitlines()[2]

    def pop_field(self, target: str) -> str | None:
        return self._data.pop(self._FIELDS_MAP[target], None)

    def get_deleted_journal_entries(self) -> list[tuple[int, int]]:
        journal_entries: list[tuple[int, int]] = []
        for field in self._IS_DELETED_FIELDS:
            value = self._data.pop(field, None)
            if value is None:
                continue

            journal_lines = value.split("; ")
            for line in journal_lines:
                journal_data = self._get_journal_data_from_line(line)
                journal_entries.append((journal_data["year"], journal_data["position"]))

        return journal_entries

    def _get_journal_data_from_line(self, journal_line: str) -> dict[str, int]:
        result = JOURNAL_LINE_PATTERN.match(journal_line)
        if not result:
            raise RuntimeError()

        return {k: int(v) for k, v in result.groupdict().items()}


class LocalGitBackend(Backend):
    def __init__(self) -> None:
        self._cursor = None
        self._repo = Repository("data/.git")
        self._journal_index: list[tuple[int, int]] = []
        self._journal_metadata: dict[tuple[int, int], JournalIndexConfig] = {}
        self._build_journal_index_and_metadata()

    def _build_journal_index_and_metadata(self) -> None:
        for commit in self._repo.walk(self._repo.head.target, GIT_SORT_REVERSE):
            metadata = Metadata(commit)
            journal_data = metadata.journal_data

            index_key = (journal_data["year"], journal_data["position"])
            self._journal_index.append(index_key)
            self._journal_metadata[index_key] = {
                "title": metadata.title,
                "commit_id": commit.short_id,
                "is_deleted": False,
                "journal_volume": journal_data["volume"],
                "promulgation_date": metadata.pop_field("promulgation_date"),
                "announcement_date": metadata.pop_field("announcement_date"),
                "comes_in_force_date": metadata.pop_field("comes_in_force_date"),
                "effective_date": metadata.pop_field("effective_date"),
            }

            deleted_journal_entries = metadata.get_deleted_journal_entries()
            for entry in deleted_journal_entries:
                self._journal_metadata[entry]["is_deleted"] = True

        self._journal_index.sort()

    def _get_legal_act(self, year: int, position: int) -> LegalAct:
        index_key = (year, position)
        if index_key not in self._journal_metadata:
            raise RuntimeError()

        act_content = None
        if not self._is_deleted(index_key):
            act_content = self._get_content(year, position)

        metadata = self._journal_metadata[index_key]
        return LegalAct(
            year=year,
            volume=metadata["journal_volume"],
            position=position,
            title=metadata["title"],
            promulgation_date=metadata["promulgation_date"],
            announcement_date=metadata["announcement_date"],
            comes_in_force_date=metadata["comes_in_force_date"],
            effective_date=metadata["effective_date"],
            content=act_content,
        )

    def _is_deleted(self, index_key: tuple[int, int]) -> bool:
        return self._journal_metadata[index_key]["is_deleted"] is True

    def _get_content(self, year: int, position: int) -> str:
        searched_filename = f"D{year}{position:>04}.md"

        data_path_glob = pathlib.Path("./data").glob("**/*.md")
        for filepath in data_path_glob:
            if filepath.name == searched_filename:
                with open(filepath) as f:
                    return f.read()

        raise RuntimeError()

    def _get_first_legal_act_index(self) -> tuple[int, int] | None:
        if not self._journal_index:
            return None
        return self._journal_index[0]

    def _get_next_legal_act_index(self) -> tuple[int, int] | None:
        if self._cursor is None:
            raise RuntimeError()
        inext = self._journal_index.index(self._cursor) + 1
        return self._journal_index[inext] if inext < len(self._journal_index) else None
