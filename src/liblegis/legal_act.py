from dataclasses import dataclass


@dataclass
class LegalAct:
    year: int
    volume: int
    position: int
    title: str
    promulgation_date: str | None
    announcement_date: str | None
    comes_in_force_date: str | None
    effective_date: str | None
    content: str | None

    @classmethod
    def from_year_and_pos(cls, year: int, position: int):
        ...

    @classmethod
    def from_filename(cls):
        ...
