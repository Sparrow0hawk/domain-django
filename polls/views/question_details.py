from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import inject
from django.forms import Form, ChoiceField, RadioSelect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from polls.domain.questions import Question, QuestionRepository


@inject.autoparams("question_repository")
def question_details(request: HttpRequest, question_id: int, question_repository: QuestionRepository) -> HttpResponse:
    question = question_repository.get(question_id)
    assert question
    if request.method == "GET":
        context = QuestionDetailContext.from_domain(question)
        return render(request, "polls/details.html", asdict(context))
    elif request.method == "POST":
        form = VoteForm.from_domain(question, request.POST)

        if not form.is_valid():
            question_details(request.GET, question_id)

        form.update_domain(question)
        question_repository.update(question)

        return HttpResponseRedirect(reverse("question_results", args=(question.id,)))
    return HttpResponse(status=405)


@dataclass(frozen=True)
class QuestionDetailContext:
    id: int
    question_text: str
    choices: VoteForm

    @classmethod
    def from_domain(cls, question: Question, *args: Any, **kwargs: Any) -> QuestionDetailContext:
        return cls(
            id=question.id,
            question_text=question.question_text,
            choices=VoteForm.from_domain(question, *args, **kwargs),
        )


class VoteForm(Form):
    choice = ChoiceField(widget=RadioSelect())

    def __init__(self, choice_options: list[str], *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        choice_field = self.fields["choice"]
        assert isinstance(choice_field, ChoiceField)
        choice_field_data = [(label, value) for label, value in zip(choice_options, choice_options)]
        choice_field.choices = choice_field_data

    @classmethod
    def from_domain(cls, question: Question, *args: Any, **kwargs: Any) -> VoteForm:
        return VoteForm([choice.choice_text for choice in question.choices], *args, **kwargs)

    def update_domain(self, question: Question) -> None:
        if self.cleaned_data["choice"]:
            question.vote_for_choice(self.cleaned_data["choice"])
