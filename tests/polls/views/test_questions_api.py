import pytest
import django.conf
from django.test import Client
from django.urls import reverse

from polls.domain.questions import QuestionRepository, Question


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
