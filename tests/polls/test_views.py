import pytest
import django.conf
from django.test import Client
from django.urls import reverse

from polls.domain.questions import QuestionRepository, Question, Choice
from tests.polls.pages import PollsPage, QuestionDetailPage


def test_index_shows_questions(config: None, client: Client, questions: QuestionRepository) -> None:
    questions.add(
        Question(id_=1, question_text="What is your favourite sandwich?"),
        Question(id_=2, question_text="What is better cat or dog?"),
    )
    url = reverse("index")
    response = client.get(url)

    polls_page = PollsPage(response)

    assert polls_page.table and polls_page.table.questions() == [
        "What is your favourite sandwich?",
        "What is better cat or dog?",
    ]


def test_index_shows_questions_no_questions(config: None, client: Client) -> None:
    url = reverse("index")
    response = client.get(url)

    polls_page = PollsPage(response)

    assert not polls_page.table and polls_page.no_questions_message


def test_index_shows_poll(config: None, client: Client, questions: QuestionRepository) -> None:
    questions.add(
        Question(id_=1, question_text="What is your favourite sandwich?"),
        Question(id_=2, question_text="What is better cat or dog?"),
    )
    url = reverse("index")
    response = client.get(url)

    polls_page = PollsPage(response)

    assert polls_page.table and polls_page.table.question_links() == ["/1/", "/2/"]


def test_question_details_shows_question(config: None, client: Client, questions: QuestionRepository) -> None:
    questions.add(Question(id_=1, question_text="What is your favourite sandwich?"))
    url = reverse("question_details", args=(1,))
    response = client.get(url)

    question_detail_page = QuestionDetailPage(response)

    assert question_detail_page.question == "What is your favourite sandwich?"


def test_question_details_shows_choices(config: None, client: Client, questions: QuestionRepository) -> None:
    question = Question(id_=1, question_text="What is your favourite sandwich?")
    question.add_choices(Choice(id_=1, choice_text="Marmite and cheese"), Choice(id_=2, choice_text="Ham and cheese"))
    questions.add(question)
    url = reverse("question_details", args=(1,))
    response = client.get(url)

    question_detail_page = QuestionDetailPage(response)

    assert question_detail_page.choices and question_detail_page.choices() == ["Marmite and cheese", "Ham and cheese"]


def test_question_details_shows_message_if_no_choices(
    config: None, client: Client, questions: QuestionRepository
) -> None:
    question = Question(id_=1, question_text="What is your favourite sandwich?")
    questions.add(question)
    url = reverse("question_details", args=(1,))
    response = client.get(url)

    question_detail_page = QuestionDetailPage(response)

    assert not question_detail_page.choices and question_detail_page.no_choices_message_visible


class TestPollsAPI:
    @pytest.fixture(name="settings_fixture", autouse=True)
    def settings(self, settings: django.conf.LazySettings) -> None:
        settings.API_KEY = "marmite"

    def test_polls_can_add_question(self, config: None, client: Client, questions: QuestionRepository) -> None:
        url = reverse("polls_questions")
        response = client.post(
            url,
            headers={"Authorization": "API-key marmite"},
            data=[{"id": 1, "question_text": "What is your favourite sandwich?"}],
            content_type="application/json",
        )

        assert response.status_code == 201
        question1 = questions.get(1)
        assert question1 and question1.id == 1 and question1.question_text == "What is your favourite sandwich?"

    def test_polls_can_add_question_with_choice(
        self, config: None, client: Client, questions: QuestionRepository
    ) -> None:
        url = reverse("polls_questions")
        response = client.post(
            url,
            headers={"Authorization": "API-key marmite"},
            data=[
                {
                    "id": 1,
                    "question_text": "What is your favourite sandwich?",
                    "choices": [{"choice_text": "Marmite and cheese"}],
                }
            ],
            content_type="application/json",
        )

        assert response.status_code == 201
        question1 = questions.get(1)
        assert question1 and question1.id == 1
        (choice1,) = question1.choices
        assert choice1.choice_text == "Marmite and cheese"

    def test_polls_can_clear_question(self, config: None, client: Client, questions: QuestionRepository) -> None:
        questions.add(Question(id_=1, question_text="What is your favourite sandwich?"))
        url = reverse("polls_questions")
        response = client.delete(url, headers={"Authorization": "API-key marmite"})

        assert response.status_code == 204
        assert not questions.get_all()

    def test_polls_cannot_add_question_when_wrong_credentials(
        self, config: None, client: Client, questions: QuestionRepository
    ) -> None:
        url = reverse("polls_questions")
        response = client.post(
            url,
            headers={"Authorization": "API-key vegemite"},
            json=[{"id": 1, "question_text": "What is your favourite sandwich?"}],
            content_type="application/json",
        )

        assert response.status_code == 401
        assert not questions.get(1)


class TestPollsAPIDisabled:
    def test_polls_cannot_add_question(self, config: None, client: Client, questions: QuestionRepository) -> None:
        url = reverse("polls_questions")
        response = client.post(
            url,
            json=[{"id": 1, "question_text": "What is your favourite sandwich?"}],
            content_type="application/json",
        )

        assert response.status_code == 401
        assert not questions.get(1)
