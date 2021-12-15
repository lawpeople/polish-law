from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol


@dataclass
class LegalActDataResult:
    year: int
    volume: int
    position: int
    title: str
    content: str


class Backend(Protocol):
    _index: list[int] | None = None

    @abstractmethod
    def get_legal_act_data(self, year: int, position: int) -> LegalActDataResult:
        ...

    @abstractmethod
    def get_next_legal_act_data(self):
        ...
