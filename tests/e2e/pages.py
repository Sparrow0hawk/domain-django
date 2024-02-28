from __future__ import annotations
from playwright.sync_api import Page


class PollsPage:
    def __init__(self, page: Page):
        self._page = page
        self._heading = self._page.get_by_role("heading")

    @classmethod
    def open(cls, page: Page, live_server_url: str) -> PollsPage:
        page.goto(live_server_url)
        return PollsPage(page)

    @property
    def heading(self) -> str | None:
        return self._heading.text_content()


class QuestionDetailPage:
    def __init__(self, page: Page):
        self._page = page
        self._question = self._page.get_by_role("heading")

    @classmethod
    def open(cls, page: Page, live_server_url: str, id_: int) -> QuestionDetailPage:
        page.goto(f"{live_server_url}/{id_}")
        return QuestionDetailPage(page)

    @property
    def question(self) -> str | None:
        return self._question.text_content()
