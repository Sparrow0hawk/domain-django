from polls.domain.questions import Question
from polls.views.index import QuestionListContext, QuestionListRowContext


class TestQuestionListContext:
    def test_from_domain(self) -> None:
        questions_list = [
            Question(id_=1, question_text="Who are you?"),
            Question(id_=2, question_text="What is your favourite sandwich?"),
        ]

        context = QuestionListContext.from_domain(questions_list)

        assert (
            context.questions[0].id == 1
            and context.questions[0].question == "Who are you?"
            and context.questions[1].id == 2
            and context.questions[1].question == "What is your favourite sandwich?"
        )


class TestQuestionListRowContext:
    def test_from_domain(self) -> None:
        context = QuestionListRowContext.from_domain(Question(id_=1, question_text="Who are you?"))

        assert context.id == 1 and context.question == "Who are you?"
