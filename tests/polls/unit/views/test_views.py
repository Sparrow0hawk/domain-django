from polls.domain.questions import Question, Choice
from polls.views import QuestionRepr, QuestionDetailContext, QuestionListContext, QuestionListRowContext, ChoiceRepr


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
