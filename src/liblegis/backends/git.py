import pathlib

from pygit2 import Repository

from liblegis.backends.base import Backend, LegalActDataResult


class LocalGitBackend(Backend):
    def __init__(self) -> None:
        self._index = None
        self._repo = Repository("data/.git")

    def get_legal_act_data(self, year: int, position: int) -> LegalActDataResult:
        commit_message = self._get_commit_message(year, position)
        act_content = self._get_content(year, position)

        journal_info, _, act_title, *meta_info = commit_message.splitlines()
        volume = int(journal_info.split()[3])
        return LegalActDataResult(year, volume, position, act_title, act_content)

    def _get_commit_message(self, year: int, position: int) -> str:
        year_part = f"Dz.U. {year}"
        pos_part = f"poz. {position}"

        for commit in self._repo.walk(self._repo.head.target):
            title_line = commit.message.splitlines()[0]
            if year_part in title_line and pos_part in title_line:
                return commit.message

        raise RuntimeError()

    def _get_content(self, year: int, position: int) -> str:
        searched_filename = f"D{year}{position:>04}.md"

        data_path_glob = pathlib.Path("./data").glob("**/*.md")
        for filepath in data_path_glob:
            if filepath.name == searched_filename:
                with open(filepath) as f:
                    return f.read()

        raise RuntimeError()

    def get_next_legal_act_data(self):
        ...
