from __future__ import annotations

from typing import Iterator, TYPE_CHECKING

from bs4 import BeautifulSoup, Tag

if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class BasePage:
    def __init__(self, response: _MonkeyPatchedWSGIResponse) -> None:
        self._soup = BeautifulSoup(response.content, "html.parser")


class PollsPage(BasePage):
    def __init__(self, response: _MonkeyPatchedWSGIResponse) -> None:
        super().__init__(response)
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


class QuestionDetailPage(BasePage):
    def __init__(self, response: _MonkeyPatchedWSGIResponse):
        super().__init__(response)
        question = self._soup.select_one("main h1")
        assert question
        self.question = question.string
        choices = self._soup.select_one("ul")
        self.choices = QuestionDetailListComponent(choices) if choices else None
        paragraph = self._soup.select_one("p")
        self.no_choices_message_visible = (
            (paragraph.string or "").strip() == "This poll has no choices." if paragraph else False
        )


class QuestionDetailListComponent:
    def __init__(self, list_: Tag):
        self._list = list_.select("li")

    def __iter__(self) -> Iterator[ListItemComponent]:
        return (ListItemComponent(item) for item in self._list)

    def __call__(self) -> list[str | None]:
        return [item.text() for item in self]


class ListItemComponent:
    def __init__(self, list_item: Tag):
        self._list_item = list_item

    def text(self) -> str | None:
        return self._list_item.string
