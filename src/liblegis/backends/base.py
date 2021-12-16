from abc import abstractmethod
from typing import Protocol

from liblegis.legal_act import LegalAct


class Backend(Protocol):
    _cursor: list[int] | None = None

    @property
    def index(self) -> list[int] | None:
        return self._cursor

    def get_legal_act(self, year: int, position: int) -> LegalAct:
        legal_act = self._get_legal_act(year, position)
        self._cursor = [year, position]
        return legal_act

    @abstractmethod
    def _get_legal_act(self, year: int, position: int) -> LegalAct:
        ...

    def get_next_legal_act(self) -> LegalAct | None:
        self._cursor = self._get_next_legal_act_index()
        year, position = self._cursor
        return self._get_legal_act(year, position)

    @abstractmethod
    def _get_next_legal_act_index(self) -> list[int]:
        ...
