from __future__ import annotations

from typing import Iterator

from playwright.sync_api import Page, Locator


class PollsPage:
    def __init__(self, page: Page):
        self._page = page
        self._heading = self._page.get_by_role("heading")
        self.table = PollsPageTableComponent(self._page.get_by_role("table"))

    @classmethod
    def open(cls, page: Page, live_server_url: str) -> PollsPage:
        page.goto(live_server_url)
        return PollsPage(page)

    @property
    def heading(self) -> str | None:
        return self._heading.text_content()


class PollsPageTableComponent:
    def __init__(self, table: Locator):
        self._table = table

    def __iter__(self) -> Iterator[PollsPageTableCellComponent]:
        return (PollsPageTableCellComponent(row) for row in self._table.get_by_role("row").all()[1:])

    def __getitem__(self, item: str) -> PollsPageTableCellComponent:
        return next(question for question in self if question.table_cell == item)

    def questions(self) -> list[str | None]:
        return [cell.table_cell for cell in self]


class PollsPageTableCellComponent:
    def __init__(self, row: Locator):
        self._cell = row.get_by_role("cell")

    @property
    def table_cell(self) -> str | None:
        return self._cell.text_content()

    def open(self) -> QuestionDetailPage:
        self._cell.get_by_role("link").click()
        return QuestionDetailPage(self._cell.page)


class QuestionDetailPage:
    def __init__(self, page: Page):
        self._page = page
        self._question = self._page.get_by_role("heading")
        main = self._page.get_by_role("main")
        self.choices = QuestionDetailFormComponent(main.get_by_role("form"))

    @classmethod
    def open(cls, page: Page, live_server_url: str, id_: int) -> QuestionDetailPage:
        page.goto(f"{live_server_url}/{id_}")
        return QuestionDetailPage(page)

    @property
    def question(self) -> str | None:
        return self._question.text_content()


class QuestionDetailFormComponent:
    def __init__(self, form: Locator):
        self._form = form
        self._submit = form.get_by_text("Vote")

    def __iter__(self) -> Iterator[RadioComponent]:
        return (RadioComponent(item, self._form) for item in self._form.get_by_role("radio").all())

    def __call__(self) -> list[str | None]:
        return [item.value for item in self]

    def __getitem__(self, item: str) -> RadioComponent:
        return next(radio_item for radio_item in self if radio_item.value == item)

    def submit(self) -> QuestionResultsPage:
        self._submit.click()
        return QuestionResultsPage(self._form.page)


class QuestionResultsPage:
    def __init__(self, page: Page):
        self._page = page
        self._question = page.get_by_role("heading")
        self._results = QuestionResultsTableComponent(self._page.get_by_role("table"))

    @property
    def question(self) -> str | None:
        return self._question.text_content()

    def results(self) -> dict[str | None, int]:
        return self._results.as_dict()


class QuestionResultsTableComponent:
    def __init__(self, table: Locator):
        self._table = table

    def __iter__(self) -> Iterator[QuestionResultsTableRowComponent]:
        return (QuestionResultsTableRowComponent(row) for row in self._table.get_by_role("row").all()[1:])

    def as_dict(self) -> dict[str | None, int]:
        return {row.choice: row.votes for row in self}


class QuestionResultsTableRowComponent:
    def __init__(self, row: Locator):
        self._row = row

    @property
    def choice(self) -> str | None:
        choice = self._row.get_by_role("cell").nth(0)
        return choice.text_content()

    @property
    def votes(self) -> int:
        votes = self._row.get_by_role("cell").nth(1)
        return int(votes.text_content() or 0)


class RadioComponent:
    def __init__(self, input_: Locator, form: Locator):
        self._input = input_
        self._form = form

    @property
    def value(self) -> str | None:
        return self._input.input_value()

    def check(self) -> QuestionDetailFormComponent:
        self._input.check()
        return QuestionDetailFormComponent(self._form)
