from polls.views import QuestionRepr


class TestQuestionRepr:
    def test_to_domain(self) -> None:
        question_repr = QuestionRepr(id=1, question_text="Who are you?")

        question = question_repr.to_domain()

        assert question.id == 1 and question.question_text == "Who are you?"
