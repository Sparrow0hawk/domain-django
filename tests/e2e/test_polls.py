from playwright.sync_api import Page
from pytest_django.live_server_helper import LiveServer

from tests.e2e.client import QuestionRepr, AppClient
from tests.e2e.pages import PollsPage, QuestionDetailPage


def test_index_shows_table(app_client: AppClient, live_server: LiveServer, page: Page) -> None:
    app_client.add_questions(
        QuestionRepr(id=1, question_text="What is the best sandwich?"),
        QuestionRepr(id=2, question_text="What is better cat or dog?"),
        QuestionRepr(id=3, question_text="What is your favourite colour?"),
    )

    polls_page = PollsPage.open(page, live_server.url)

    assert polls_page.heading == "Polls"
    assert polls_page.table.questions() == [
        "What is the best sandwich?",
        "What is better cat or dog?",
        "What is your favourite colour?",
    ]


def test_index_shows_poll(app_client: AppClient, live_server: LiveServer, page: Page) -> None:
    app_client.add_questions(QuestionRepr(id=1, question_text="What is the best sandwich?"))

    question_detail_page = PollsPage.open(page, live_server.url).table["What is the best sandwich?"].open()

    assert question_detail_page.question == "What is the best sandwich?"


def test_poll_shows_question(app_client: AppClient, live_server: LiveServer, page: Page) -> None:
    app_client.add_questions(QuestionRepr(id=1, question_text="What is the best sandwich?"))

    question_detail_page = QuestionDetailPage.open(page, live_server.url, 1)

    assert question_detail_page.question == "What is the best sandwich?"
