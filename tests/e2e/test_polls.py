from dataclasses import dataclass, asdict

import requests
from playwright.sync_api import Page
from pytest_django.live_server_helper import LiveServer

from tests.e2e.pages import PollsPage, QuestionDetailPage


def test_index_shows_header(live_server: LiveServer, page: Page) -> None:
    polls_page = PollsPage.open(page, live_server.url)

    assert polls_page.heading == "Hello world!"


def test_poll_shows_question(live_server: LiveServer, page: Page) -> None:
    json = [asdict(QuestionRepr(id=1, question_text="What is the best sandwich?"))]
    response = requests.post(f"{live_server.url}/polls/questions", json=json, timeout=10)
    response.raise_for_status()

    question_detail_page = QuestionDetailPage.open(page, live_server.url, 1)

    assert question_detail_page.question == "What is the best sandwich?"


@dataclass
class QuestionRepr:
    id: int
    question_text: str
