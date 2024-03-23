from django.test import Client
from django.urls import reverse

from polls.domain.questions import QuestionRepository, Question, Choice
from tests.polls.views.pages import QuestionDetailPage


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
