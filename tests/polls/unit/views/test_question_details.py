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
    def test_create(self) -> None:
        form = VoteForm(choice_options=["John Smith", "Jane Smith"])
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
