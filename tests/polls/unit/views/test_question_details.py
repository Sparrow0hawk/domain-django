from polls.domain.questions import Question, Choice
from polls.views.question_details import QuestionDetailContext


class TestQuestionDetailContext:
    def test_from_domain(self) -> None:
        question = Question(id_=1, question_text="Who are you?")

        context = QuestionDetailContext.from_domain(question)

        assert context.question_text == "Who are you?" and not context.choices

    def test_from_domain_sets_choices(self) -> None:
        question = Question(id_=1, question_text="Who are you?")
        question.add_choices(Choice(id_=1, choice_text="John Smith"))

        context = QuestionDetailContext.from_domain(question)

        assert context.question_text == "Who are you?" and context.choices == ["John Smith"]
