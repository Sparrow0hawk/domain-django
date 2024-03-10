from __future__ import annotations
from dataclasses import dataclass, asdict

import requests


class AppClient:
    DEFAULT_TIMEOUT = 10

    def __init__(self, url: str):
        self._url = url
        self._session = requests.Session()

    def add_questions(self, *questions: QuestionRepr) -> None:
        json = [asdict(question) for question in questions]
        response = self._session.post(f"{self._url}/polls/questions", json=json, timeout=self.DEFAULT_TIMEOUT)
        response.raise_for_status()

    def clear_questions(self) -> None:
        response = self._session.delete(f"{self._url}/polls/questions", timeout=self.DEFAULT_TIMEOUT)
        response.raise_for_status()


@dataclass
class QuestionRepr:
    id: int
    question_text: str
