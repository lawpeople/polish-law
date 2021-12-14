import pathlib
import re
from typing import Generator

import pytest

BASE_DIRS = ["data/Królestwo", "data/IIRP"]

LEGAL_ARTICLE_NO_PATTERN: re.Pattern[str] = re.compile(r"Art\. (\d+)\.")
LEGAL_ARTICLE_PATTERN: re.Pattern[str] = re.compile(
    r"Art\. (\d+)\. ((?:[\S ]+\n?)+)(\n*)"
)


def is_roman_numeric(text: str) -> bool:
    # Very naive check, however there is no need to validate
    return set(text).issubset(set("IVXLCDM"))


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
    yield content


def test_articles_correct_count_and_order(legal_act: str):
    legal_article_nums = [int(n) for n in LEGAL_ARTICLE_NO_PATTERN.findall(legal_act)]
    if not legal_article_nums:
        return

    expected_count = legal_article_nums[-1]
    actual_count = len(legal_article_nums)
    if expected_count != actual_count:
        pytest.fail(
            "Legal articles count check failed\n"
            f"Expected {expected_count} articles but found {actual_count}"
        )

    article_range_end = legal_article_nums[-1] + 1
    for ix, expected in enumerate(range(1, article_range_end)):
        found = legal_article_nums[ix]
        if found != expected:
            pytest.fail(
                "Legal articles order check failed\n"
                f"Expected 'Art. {expected}. [...]'\n"
                f"Found 'Art. {found}. [...]'"
            )


def test_articles_correct_structure(legal_act: str):
    legal_article_matches = LEGAL_ARTICLE_PATTERN.findall(legal_act)
    if not legal_article_matches:
        return

    expected_count = int(legal_article_matches[-1][0])
    assert len(legal_article_matches) == expected_count

    for legal_article_match in legal_article_matches:
        article_no = legal_article_match[0]
        article_text = legal_article_match[1]
        whitespacing_after = legal_article_match[2]

        article_linebreaks = re.findall(r"( +\n+)", article_text)
        for linebreak in article_linebreaks:
            if linebreak != "  \n":
                pytest.fail(f"Incorrect linebreak structure in Art. {article_no}")

        if not article_text.endswith("\n") or not whitespacing_after:
            pytest.fail(f"Missing newline after Art. {article_no}")
        if "\n" in whitespacing_after and whitespacing_after != "\n":
            pytest.fail(f"Too many newlines after Art. {article_no}")


def test_ordered_list_members_correct_order(legal_act: str):
    ordered_lists: list[list[int]] = []
    is_ordered_list = False
    for line in legal_act.splitlines():
        results = [int(n) for n in re.findall(r"(\d+)\\[\.\)]", line)]
        if not is_ordered_list and results:
            ordered_lists.append(results)
            is_ordered_list = True
        elif is_ordered_list and results:
            ordered_lists[-1].extend(results)
        elif line.strip() == "":
            is_ordered_list = False

    for indices in ordered_lists:
        index_range_end = len(indices) + 1
        expected_indices = list(range(1, index_range_end))
        if expected_indices != indices:
            expected_lines = "\n".join(
                [f"{num}\\[.)] [...]" for num in expected_indices]
            )
            found_lines = "\n".join([f"{num}\\[.)] [...]" for num in indices])
            pytest.fail(
                "Ordered list members check failed\n"
                "Expected:\n"
                f"{expected_lines}"
                "\n\nFound:\n"
                f"{found_lines}"
            )


def test_ordered_list_members_correct_escaping(legal_act: str):
    ordered_list_members = re.findall(r"\n(\d+(\\?)[\.\)][\S ]+)", legal_act)
    for list_member, escape_slash in ordered_list_members:
        if escape_slash != "\\":
            pytest.fail(f"List member is not escaped:\n{list_member}")


def test_spacing_between_words(legal_act: str):
    invalid_spacing_results = re.findall(r"([^ \n\|—]+)( {2,})([^ \n\|—]+)", legal_act)
    for first_word, spacing, second_word in invalid_spacing_results:
        pytest.fail(
            "Incorrect spacing between words\n"
            f"Found: '{first_word}{spacing}{second_word}'\n"
            f"Expected: '{first_word} {second_word}'"
        )


def test_spacing_between_emdash(legal_act: str):
    emdash_results = re.findall(r"(\S+)(\s*)—(\s*)(\S+)", legal_act)
    for text_before, spacing_before, spacing_after, text_after in emdash_results:
        if "\n" in spacing_after:
            continue

        if text_before == "|" and text_after == "|":
            continue

        if text_before.isdigit() and text_after.isdigit():
            continue

        if is_roman_numeric(text_before) and is_roman_numeric(text_after):
            continue

        if spacing_before != " " or spacing_after != " ":
            pytest.fail(
                "Incorrect spacing between emdash\n"
                f"Found: '{text_before}{spacing_before}—{spacing_after}{text_after}'\n"
                f"Expected: '{text_before} — {text_after}'"
            )
