from abc import abstractmethod

from liblegis.legal_act import LegalAct


class Backend:
    _cursor: tuple[int, int] | None

    def __init__(self, parse_content: bool = False) -> None:
        self._cursor = None
        self._parse_content = parse_content

    @property
    def cursor(self) -> tuple[int, int] | None:
        return self._cursor

    def _get_processed_legal_act(self, year: int, position: int) -> LegalAct:
        legal_act = self._get_legal_act(year, position)
        if self._parse_content:
            legal_act.parse_content()

        return legal_act

    def get_legal_act(self, year: int, position: int) -> LegalAct:
        legal_act = self._get_processed_legal_act(year, position)
        self._cursor = (year, position)
        return legal_act

    def get_first_legal_act(self) -> LegalAct | None:
        self._cursor = self._get_first_legal_act_index()
        if self._cursor is None:
            return None
        year, position = self._cursor
        return self._get_processed_legal_act(year, position)

    @abstractmethod
    def _get_legal_act(self, year: int, position: int) -> LegalAct:
        ...

    def get_next_legal_act(self) -> LegalAct | None:
        self._cursor = self._get_next_legal_act_index()
        if self._cursor is None:
            return None
        year, position = self._cursor
        return self._get_processed_legal_act(year, position)

    @abstractmethod
    def _get_first_legal_act_index(self) -> tuple[int, int] | None:
        ...

    @abstractmethod
    def _get_next_legal_act_index(self) -> tuple[int, int] | None:
        ...
