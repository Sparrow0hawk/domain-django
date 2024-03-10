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
        self.choices = QuestionDetailListComponent(self._page.get_by_role("list"))

    @classmethod
    def open(cls, page: Page, live_server_url: str, id_: int) -> QuestionDetailPage:
        page.goto(f"{live_server_url}/{id_}")
        return QuestionDetailPage(page)

    @property
    def question(self) -> str | None:
        return self._question.text_content()


class QuestionDetailListComponent:
    def __init__(self, list_: Locator):
        self._list = list_

    def __iter__(self) -> Iterator[ListItemComponent]:
        return (ListItemComponent(item) for item in self._list.get_by_role("listitem").all())

    def __call__(self) -> list[str | None]:
        return [item.text for item in self]


class ListItemComponent:
    def __init__(self, list_item: Locator):
        self._list_item = list_item

    @property
    def text(self) -> str | None:
        return self._list_item.text_content()
