from __future__ import annotations
import json
from dataclasses import dataclass, asdict

import inject
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from polls.domain.questions import Question, QuestionRepository


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


@inject.autoparams("questions")
def index(request: HttpRequest, questions: QuestionRepository) -> HttpResponse:
    all_questions = questions.get_all()

    context = QuestionListContext.from_domain(all_questions)

    return render(request, "polls/index.html", asdict(context))


@dataclass
class QuestionRepr:
    id: int
    question_text: str

    def to_domain(self) -> Question:
        return Question(id_=self.id, question_text=self.question_text)


@csrf_exempt
@inject.autoparams("questions")
def questions_api(request: HttpRequest, questions: QuestionRepository) -> HttpResponse:
    if request.method == "POST":
        payload = json.loads(request.body)
        questions_repr = [QuestionRepr(**element) for element in payload]
        questions.add(*[question_repr.to_domain() for question_repr in questions_repr])
        return HttpResponse(status=201)
    elif request.method == "DELETE":
        questions.clear()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)


@dataclass(frozen=True)
class QuestionDetailContext:
    question_text: str

    @classmethod
    def from_domain(cls, question: Question) -> QuestionDetailContext:
        return cls(question_text=question.question_text)


@inject.autoparams("question_repository")
def question_details(request: HttpRequest, question_id: int, question_repository: QuestionRepository) -> HttpResponse:
    question = question_repository.get(question_id)
    assert question

    context = QuestionDetailContext.from_domain(question)
    return render(request, "polls/details.html", asdict(context))
