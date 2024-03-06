from __future__ import annotations

from typing import Iterator, TYPE_CHECKING

from bs4 import BeautifulSoup, Tag

if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class PollsPage:
    def __init__(self, response: _MonkeyPatchedWSGIResponse) -> None:
        self._soup = BeautifulSoup(response.content, "html.parser")
        table = self._soup.select_one("main table")
        self.table = PollsPageTableComponent(table) if table else None
        paragraph = self._soup.select_one("main h1 ~ p")
        self.no_questions_message = paragraph.string == "No questions to view." if paragraph else None


class PollsPageTableComponent:
    def __init__(self, table: Tag):
        self._rows = table.select("tbody tr")

    def __iter__(self) -> Iterator[PollsPageTableCellComponent]:
        return (PollsPageTableCellComponent(row) for row in self._rows)

    def questions(self) -> list[str | None]:
        return [cell.table_cell for cell in self]

    def question_links(self) -> list[str | list[str] | None]:
        return [cell.question_url for cell in self]


class PollsPageTableCellComponent:
    def __init__(self, row: Tag):
        cell = row.select_one("td")
        assert cell
        self._cell = cell
        question_url = cell.select_one("a")
        assert question_url
        self.question_url = question_url.get("href")

    @property
    def table_cell(self) -> str | None:
        return self._cell.string
