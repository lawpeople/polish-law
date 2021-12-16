import pathlib
import re

import pytest

LEGAL_ACT_FILENAME_PATTERN = re.compile(r"D(\d{4})(\d{4})")


def test_article_file_path_structure(legal_act_file_path: pathlib.Path):
    match_result = LEGAL_ACT_FILENAME_PATTERN.match(legal_act_file_path.stem)
    if match_result is None:
        pytest.fail(
            "Legal act filename should follow the following pattern: "
            "'D[4-digit year][0-prefixed 4-digit position].md'"
        )
    year, _ = match_result.groups()
    assert 1918 <= int(year) <= 2021

    assert legal_act_file_path.suffix == ".md"


def test_no_duplicate_file_name_exists(all_legal_act_file_paths: list[pathlib.Path]):
    file_names = [path.name for path in all_legal_act_file_paths]
    assert len(set(file_names)) == len(file_names)
