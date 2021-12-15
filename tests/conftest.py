import pathlib
from typing import Generator

import pytest

BASE_DIRS = ["data/Królestwo", "data/IIRP"]


def _gather_legal_act_file_paths():
    root_path = pathlib.Path(".")

    for base_dir in BASE_DIRS:
        legal_acts_path = root_path / base_dir
        for file_path in legal_acts_path.glob("**/*.md"):
            yield pytest.param(file_path, id=file_path.name)


@pytest.fixture(scope="session", params=_gather_legal_act_file_paths())
def legal_act(request: pytest.FixtureRequest) -> Generator[str, None, None]:
    with open(request.param) as f:
        content = f.read()
    return content


@pytest.fixture(scope="session", params=_gather_legal_act_file_paths())
def legal_act_file_path(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture(scope="session")
def all_legal_act_file_paths():
    return [param.values[0] for param in _gather_legal_act_file_paths()]
