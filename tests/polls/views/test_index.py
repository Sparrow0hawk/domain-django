from django.test import Client
from django.urls import reverse

from polls.domain.questions import QuestionRepository, Question
from tests.polls.views.pages import PollsPage


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
