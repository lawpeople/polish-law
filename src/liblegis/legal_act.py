import re
from dataclasses import dataclass

LEGAL_ARTICLE_PATTERN: re.Pattern[str] = re.compile(
    r"Art\. (\d+)\. ((?:[\S ]+\n?)+)\n*"
)


@dataclass
class LegalArticle:
    number: int
    content: str


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
    articles: list[LegalArticle]

    def parse_content(self) -> None:
        if not self.content:
            return

        data: list[tuple[str, str]] = LEGAL_ARTICLE_PATTERN.findall(self.content)
        self.articles = [
            LegalArticle(number=int(article_data[0]), content=article_data[1].strip())
            for article_data in data
        ]
