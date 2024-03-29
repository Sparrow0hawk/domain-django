from __future__ import annotations

from dataclasses import dataclass, field, asdict

import inject
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
        choice = request.POST["choice"]
        question.vote_for_choice(choice_text=choice)
        question_repository.update(question)
        return HttpResponseRedirect(reverse("question_results", args=(question.id,)))
    return HttpResponse(status=405)


@dataclass(frozen=True)
class QuestionDetailContext:
    id: int
    question_text: str
    choices: list[str] = field(default_factory=list)

    @classmethod
    def from_domain(cls, question: Question) -> QuestionDetailContext:
        return cls(
            id=question.id,
            question_text=question.question_text,
            choices=[choice.choice_text for choice in question.choices],
        )
