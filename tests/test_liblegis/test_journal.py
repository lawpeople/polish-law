import pytest

from liblegis import Journal
from liblegis.backends import Backend


@pytest.mark.parametrize("mock_backend", [{}], indirect=True)
def test_empty_journal(mock_backend: Backend):
    journal = Journal(mock_backend)
    acts = [act for act in journal]
    assert acts == []


@pytest.mark.parametrize(
    "mock_backend",
    [
        {
            (2022, 3): {
                "volume": 1,
                "title": "Foo",
                "promulgation_date": "2022-02-10",
                "announcement_date": "2022-02-14",
                "comes_in_force_date": "2022-02-16",
                "effective_date": "2022-02-18",
                "content": "Foo content",
            }
        }
    ],
    indirect=True,
)
def test_journal_single_act(mock_backend: Backend):
    journal = Journal(mock_backend)
    acts = [act for act in journal]
    assert len(acts) == 1

    assert acts[0].year == 2022
    assert acts[0].position == 3
    assert acts[0].volume == 1
    assert acts[0].title == "Foo"
    assert acts[0].promulgation_date == "2022-02-10"
    assert acts[0].announcement_date == "2022-02-14"
    assert acts[0].comes_in_force_date == "2022-02-16"
    assert acts[0].effective_date == "2022-02-18"
    assert acts[0].content == "Foo content"
