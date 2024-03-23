from polls.views.question_api import QuestionRepr, ChoiceRepr


class TestQuestionRepr:
    def test_to_domain(self) -> None:
        question_repr = QuestionRepr(id=1, question_text="Who are you?")

        question = question_repr.to_domain()

        assert question.id == 1 and question.question_text == "Who are you?" and not question.choices

    def test_to_domain_sets_choices(self) -> None:
        question_repr = QuestionRepr(
            id=1, question_text="Who are you?", choices=[ChoiceRepr(id=1, choice_text="John Smith")]
        )

        question = question_repr.to_domain()

        assert (
            question.id == 1
            and question.question_text == "Who are you?"
            and question.choices[0].choice_text == "John Smith"
        )


class TestChoiceRepr:
    def test_to_domain(self) -> None:
        choice_repr = ChoiceRepr(id=1, choice_text="Marmite and cheese")

        choice = choice_repr.to_domain()

        assert choice.id == 1 and choice.choice_text == "Marmite and cheese"
