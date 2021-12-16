from dataclasses import dataclass


@dataclass
class LegalAct:
    year: int
    volume: int
    position: int
    title: str
    content: str | None

    @classmethod
    def from_year_and_pos(cls, year: int, position: int):
        ...

    @classmethod
    def from_filename(cls):
        ...
