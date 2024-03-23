from playwright.sync_api import Page
from pytest_django.live_server_helper import LiveServer

from tests.e2e.client import AppClient, QuestionRepr, ChoiceRepr
from tests.e2e.pages import PollsPage


def test_question_details_shows_question_and_choices(
    app_client: AppClient, live_server: LiveServer, page: Page
) -> None:
    app_client.add_questions(
        QuestionRepr(
            id=1,
            question_text="What is the best sandwich?",
            choices=[
                ChoiceRepr(id=1, choice_text="Marmite and cheese"),
                ChoiceRepr(id=2, choice_text="Ham and cheese"),
                ChoiceRepr(id=3, choice_text="Cheese"),
            ],
        )
    )

    question_detail_page = PollsPage.open(page, live_server.url).table["What is the best sandwich?"].open()

    assert question_detail_page.question == "What is the best sandwich?"
    assert question_detail_page.choices() == ["Marmite and cheese", "Ham and cheese", "Cheese"]
