from __future__ import annotations
import json
from dataclasses import dataclass, asdict, field

import inject
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pydantic.dataclasses import dataclass as pydantic_dataclass

from polls.auth import api_key_auth
from polls.domain.questions import Question, QuestionRepository, Choice


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


@pydantic_dataclass
class QuestionRepr:
    id: int
    question_text: str
    choices: list[ChoiceRepr] = field(default_factory=list)

    def to_domain(self) -> Question:
        question = Question(id_=self.id, question_text=self.question_text)
        question.add_choices(*[answer.to_domain() for answer in self.choices])
        return question


@pydantic_dataclass
class ChoiceRepr:
    choice_text: str
    id: int | None = None

    def to_domain(self) -> Choice:
        return Choice(id_=self.id, choice_text=self.choice_text)


@csrf_exempt
@api_key_auth
@inject.autoparams("questions")
def questions_api(request: HttpRequest, questions: QuestionRepository) -> HttpResponse:
    if request.method == "POST":
        payload = json.loads(request.body)
        questions_reprs = [QuestionRepr(**element) for element in payload]
        questions.add(*[question_repr.to_domain() for question_repr in questions_reprs])
        return HttpResponse(status=201)
    elif request.method == "DELETE":
        questions.clear()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)


@dataclass(frozen=True)
class QuestionDetailContext:
    question_text: str
    choices: list[str] = field(default_factory=list)

    @classmethod
    def from_domain(cls, question: Question) -> QuestionDetailContext:
        return cls(question_text=question.question_text, choices=[choice.choice_text for choice in question.choices])


@inject.autoparams("question_repository")
def question_details(request: HttpRequest, question_id: int, question_repository: QuestionRepository) -> HttpResponse:
    question = question_repository.get(question_id)
    assert question

    context = QuestionDetailContext.from_domain(question)
    return render(request, "polls/details.html", asdict(context))
