from django.test import Client
from django.urls import reverse

from polls.domain.questions import QuestionRepository, Question, Choice
from tests.polls.views.pages import QuestionResultsPage


def test_question_results_shows_votes(config: None, client: Client, questions: QuestionRepository) -> None:
    question = Question(id_=1, question_text="What is your favourite sandwich?")
    question.add_choices(
        Choice(id_=1, choice_text="Marmite and cheese", votes=2), Choice(id_=2, choice_text="Ham and cheese", votes=3)
    )
    questions.add(question)

    url = reverse("question_results", args=(1,))
    response = client.post(url)

    question_results_page = QuestionResultsPage(response)

    assert question_results_page.results and question_results_page.results() == {
        "Marmite and cheese": 2,
        "Ham and cheese": 3,
    }
