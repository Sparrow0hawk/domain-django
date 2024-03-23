from __future__ import annotations

from dataclasses import dataclass, field, asdict

import inject
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from polls.domain.questions import Question, QuestionRepository


@inject.autoparams("question_repository")
def question_details(request: HttpRequest, question_id: int, question_repository: QuestionRepository) -> HttpResponse:
    question = question_repository.get(question_id)
    assert question

    context = QuestionDetailContext.from_domain(question)
    return render(request, "polls/details.html", asdict(context))


@dataclass(frozen=True)
class QuestionDetailContext:
    question_text: str
    choices: list[str] = field(default_factory=list)

    @classmethod
    def from_domain(cls, question: Question) -> QuestionDetailContext:
        return cls(question_text=question.question_text, choices=[choice.choice_text for choice in question.choices])
