from polls.domain.questions import Question, Choice
from polls.views.question_results import QuestionResultsContext, QuestionResultsRowContext


class TestQuestionResultsContext:
    def test_from_domain(self) -> None:
        question = Question(id_=1, question_text="Who are you?")

        context = QuestionResultsContext.from_domain(question)

        assert context.question_text == "Who are you?" and not context.choices

    def test_from_domain_sets_choices(self) -> None:
        question = Question(id_=1, question_text="Who are you?")
        question.add_choices(Choice(id_=1, choice_text="John Smith", votes=2))

        context = QuestionResultsContext.from_domain(question)

        assert context.question_text == "Who are you?"

        choice1: QuestionResultsRowContext
        (choice1,) = context.choices
        assert choice1.choice_text == "John Smith" and choice1.votes == 2


class TestQuestionResultsRowContext:
    def test_from_domain(self) -> None:
        choice = Choice(id_=1, choice_text="John Smith", votes=10)

        context = QuestionResultsRowContext.from_domain(choice)

        assert context.choice_text == "John Smith" and context.votes == 10
