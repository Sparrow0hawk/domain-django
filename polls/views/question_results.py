from __future__ import annotations

from dataclasses import dataclass, field, asdict

import inject
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from polls.domain.questions import Question, Choice, QuestionRepository


@inject.autoparams("question_repository")
def question_results(request: HttpRequest, question_id: int, question_repository: QuestionRepository) -> HttpResponse:
    question = question_repository.get(question_id)
    assert question

    context = QuestionResultsContext.from_domain(question)

    return render(request, "polls/results.html", asdict(context))


@dataclass(frozen=True)
class QuestionResultsContext:
    question_text: str
    choices: list[QuestionResultsRowContext] = field(default_factory=list)

    @classmethod
    def from_domain(cls, question: Question) -> QuestionResultsContext:
        return cls(
            question_text=question.question_text,
            choices=[QuestionResultsRowContext.from_domain(choice) for choice in question.choices],
        )


@dataclass
class QuestionResultsRowContext:
    choice_text: str
    votes: int

    @classmethod
    def from_domain(cls, choice: Choice) -> QuestionResultsRowContext:
        return cls(choice_text=choice.choice_text, votes=choice.votes)
