from django.forms import ChoiceField

from polls.domain.questions import Question, Choice
from polls.views.question_details import QuestionDetailContext, VoteForm


class TestQuestionDetailContext:
    def test_from_domain(self) -> None:
        question = Question(id_=1, question_text="Who are you?")

        context = QuestionDetailContext.from_domain(question)
        context_choice_field = context.choices.fields["choice"]

        assert (
            context.id == 1
            and context.question_text == "Who are you?"
            and isinstance(context_choice_field, ChoiceField)
            and not context_choice_field.choices
        )

    def test_from_domain_sets_choices(self) -> None:
        question = Question(id_=1, question_text="Who are you?")
        question.add_choices(Choice(id_=1, choice_text="John Smith", votes=0))

        context = QuestionDetailContext.from_domain(question)
        context_choice_field = context.choices.fields["choice"]

        assert (
            context.id == 1
            and context.question_text == "Who are you?"
            and isinstance(context_choice_field, ChoiceField)
            and context_choice_field.choices == [("John Smith", "John Smith")]
        )


class TestVoteForm:
    def test_from_domain(self) -> None:
        question = Question(id_=1, question_text="Who are you?")
        question.add_choices(
            Choice(id_=2, choice_text="John Smith", votes=0), Choice(id_=3, choice_text="Jane Smith", votes=0)
        )

        form = VoteForm.from_domain(question)
        form_choice_field = form.fields["choice"]

        assert (
            "choice" in form.fields
            and isinstance(form_choice_field, ChoiceField)
            and form_choice_field.choices
            == [
                ("John Smith", "John Smith"),
                ("Jane Smith", "Jane Smith"),
            ]
        )

    def test_update_domain(self) -> None:
        question = Question(id_=1, question_text="Who are you?")
        question.add_choices(
            Choice(id_=2, choice_text="John Smith", votes=0), Choice(id_=3, choice_text="Jane Smith", votes=0)
        )

        form = VoteForm.from_domain(question, data={"choice": "John Smith"})
        form.is_valid()
        form.update_domain(question)

        choice1: Choice
        choice2: Choice
        (choice1, choice2) = question.choices
        assert choice1.id == 2 and choice1.votes == 1 and choice2.id == 3 and choice2.votes == 0

    def test_form_choice_must_be_a_choice(self) -> None:
        question = Question(id_=1, question_text="Who are you?")
        question.add_choices(
            Choice(id_=2, choice_text="John Smith", votes=0), Choice(id_=3, choice_text="Jane Smith", votes=0)
        )

        form = VoteForm.from_domain(question, data={"choice": "Rob Smith"})

        form.is_valid()

        assert "Select a valid choice. Rob Smith is not one of the available choices." in form.errors["choice"]
