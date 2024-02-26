from dataclasses import dataclass, asdict

import requests
from playwright.sync_api import Page
from pytest_django.live_server_helper import LiveServer


def test_index_shows_header(live_server: LiveServer, page: Page) -> None:
    page.goto(live_server.url)

    index_heading = page.get_by_role("heading")

    assert index_heading.text_content() == "Hello world!"


def test_poll_shows_question(live_server: LiveServer, page: Page) -> None:
    json = [asdict(QuestionRepr(id=1, question_text="What is the best sandwich?"))]
    response = requests.post(f"{live_server.url}/polls/questions", json=json, timeout=10)
    response.raise_for_status()
    page.goto(f"{live_server.url}/1")

    poll_question = page.get_by_role("main").get_by_role("heading")

    assert poll_question.text_content() == "What is the best sandwich?"


@dataclass
class QuestionRepr:
    id: int
    question_text: str
