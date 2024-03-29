from __future__ import annotations

import json
from dataclasses import field

import inject
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pydantic.dataclasses import dataclass as pydantic_dataclass

from polls.auth import api_key_auth
from polls.domain.questions import Question, Choice, QuestionRepository


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
    votes: int = 0

    def to_domain(self) -> Choice:
        return Choice(id_=self.id, choice_text=self.choice_text, votes=self.votes)
