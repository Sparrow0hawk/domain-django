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
        choices = self._soup.select_one("main form")
        self.choices = QuestionDetailFormComponent(choices) if choices else None
        paragraph = self._soup.select_one("p")
        self.no_choices_message_visible = (
            (paragraph.string or "").strip() == "This poll has no choices." if paragraph else False
        )


class QuestionDetailFormComponent:
    def __init__(self, form: Tag):
        self._inputs = form.select("input")

    def __iter__(self) -> Iterator[RadioComponent]:
        return (RadioComponent(input_) for input_ in self._inputs if input_["type"] == "radio")

    def __call__(self) -> list[str | list[str] | None]:
        return [item.value for item in self]


class RadioComponent:
    def __init__(self, input_: Tag):
        self._list_item = input_
        self.value = input_.get("value")


class QuestionResultsPage(BasePage):
    def __init__(self, response: _MonkeyPatchedWSGIResponse):
        super().__init__(response)
        question = self._soup.select_one("main h1")
        assert question
        self.question = question.string
        results = self._soup.select_one("table")
        self.results = QuestionResultsTableComponent(results) if results else None


class QuestionResultsTableComponent:
    def __init__(self, table: Tag):
        self._rows = table.select("tbody tr")

    def __iter__(self) -> Iterator[QuestionResultsTableRowComponent]:
        return (QuestionResultsTableRowComponent(row) for row in self._rows)

    def __call__(self) -> dict[str | None, int]:
        return {row.choice: row.votes for row in self}


class QuestionResultsTableRowComponent:
    def __init__(self, row: Tag):
        cells = row.select("td")
        self.choice = cells[0].string
        votes = cells[1].string
        assert votes
        self.votes = int(votes)
