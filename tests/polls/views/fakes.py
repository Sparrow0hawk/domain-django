from typing import Dict

from polls.domain.questions import QuestionRepository, Question


class MemoryQuestionRepository(QuestionRepository):
    def __init__(self) -> None:
        self._questions: Dict[int, Question] = {}

    def add(self, *questions: Question) -> None:
        for question in questions:
            self._questions[question.id] = question

    def get(self, id_: int) -> Question | None:
        return self._questions.get(id_)

    def get_all(self) -> list[Question]:
        return [question for question in self._questions.values()]

    def update(self, question: Question) -> None:
        self._questions[question.id] = question

    def clear(self) -> None:
        self._questions.clear()
