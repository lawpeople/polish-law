from typing import TypedDict

import pytest

from liblegis.backends import Backend
from liblegis.legal_act import LegalAct, LegalArticle


class MockBackendDataEntry(TypedDict):
    volume: int
    title: str
    promulgation_date: str
    announcement_date: str
    comes_in_force_date: str
    effective_date: str
    content: str
    articles: list[LegalArticle]


MockBackendData = dict[tuple[int, int], MockBackendDataEntry]


class MockBackendFixtureRequest:
    param: MockBackendData


class MockBackend(Backend):
    def __init__(self, data: MockBackendData) -> None:
        super().__init__()
        self._indices = sorted(data.keys())
        self._data = data

    def _get_legal_act(self, year: int, position: int) -> LegalAct:
        act_data = self._data[year, position]
        return LegalAct(year=year, position=position, **act_data)

    def _get_first_legal_act_index(self) -> tuple[int, int] | None:
        if not self._indices:
            return None
        return self._indices[0]

    def _get_next_legal_act_index(self) -> tuple[int, int] | None:
        if self._cursor is None:
            raise RuntimeError()
        inext = self._indices.index(self._cursor) + 1
        return self._indices[inext] if inext < len(self._indices) else None


@pytest.fixture(scope="function")
def mock_backend(request: MockBackendFixtureRequest):
    return MockBackend(data=request.param)
