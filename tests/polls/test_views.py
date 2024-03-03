from django.test import Client
from django.urls import reverse

from polls.domain.questions import QuestionRepository, Question
from tests.polls.pages import PollsPage


def test_index_shows_header(config: None, client: Client, questions: QuestionRepository) -> None:
    questions.add(
        Question(id_=1, question_text="What is your favourite sandwich?"),
        Question(id_=2, question_text="What is better cat or dog?"),
    )
    url = reverse("index")
    response = client.get(url)

    polls_page = PollsPage(response)

    assert polls_page.table.questions() == ["What is your favourite sandwich?", "What is better cat or dog?"]


def test_index_shows_poll(config: None, client: Client, questions: QuestionRepository) -> None:
    questions.add(
        Question(id_=1, question_text="What is your favourite sandwich?"),
        Question(id_=2, question_text="What is better cat or dog?"),
    )
    url = reverse("index")
    response = client.get(url)

    polls_page = PollsPage(response)

    assert polls_page.table.question_links() == ["/1/", "/2/"]


def test_question_details_shows_question(config: None, client: Client, questions: QuestionRepository) -> None:
    questions.add(Question(id_=1, question_text="What is your favourite sandwich?"))
    url = reverse("question_details", args=(1,))
    response = client.get(url)

    assert b"<h1>What is your favourite sandwich?</h1>" in response.content


class TestPollsAPI:
    def test_polls_can_add_question(self, config: None, client: Client, questions: QuestionRepository) -> None:
        url = reverse("polls_questions")
        response = client.post(
            url,
            [{"id": 1, "question_text": "What is your favourite sandwich?"}],
            content_type="application/json",
        )

        assert response.status_code == 201
        question1 = questions.get(1)
        assert question1 and question1.id == 1 and question1.question_text == "What is your favourite sandwich?"
