from __future__ import annotations


class Question:
    def __init__(self, id_: int, question_text: str):
        self.id = id_
        self.question_text = question_text
        self.choices: list[Choice] = []

    def add_choices(self, *choices: Choice) -> None:
        for choice in choices:
            self.choices.append(choice)


class Choice:
    def __init__(self, id_: int | None, choice_text: str):
        self.id = id_
        self.choice_text = choice_text


class QuestionRepository:
    def add(self, *question: Question) -> None:
        raise NotImplementedError()

    def get(self, id_: int) -> Question | None:
        raise NotImplementedError()

    def get_all(self) -> list[Question]:
        raise NotImplementedError()

    def clear(self) -> None:
        raise NotImplementedError()
