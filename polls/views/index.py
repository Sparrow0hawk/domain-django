from __future__ import annotations

from dataclasses import asdict, dataclass

import inject
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from polls.domain.questions import QuestionRepository, Question


@inject.autoparams("questions")
def index(request: HttpRequest, questions: QuestionRepository) -> HttpResponse:
    all_questions = questions.get_all()

    context = QuestionListContext.from_domain(all_questions)

    return render(request, "polls/index.html", asdict(context))


@dataclass
class QuestionListContext:
    questions: list[QuestionListRowContext]

    @classmethod
    def from_domain(cls, questions_list: list[Question]) -> QuestionListContext:
        return cls(questions=[QuestionListRowContext.from_domain(question) for question in questions_list])


@dataclass
class QuestionListRowContext:
    id: int
    question: str

    @classmethod
    def from_domain(cls, question: Question) -> QuestionListRowContext:
        return cls(id=question.id, question=question.question_text)
