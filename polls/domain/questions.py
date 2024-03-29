from __future__ import annotations


class Question:
    def __init__(self, id_: int, question_text: str):
        self.id = id_
        self.question_text = question_text
        self.choices: list[Choice] = []

    def add_choices(self, *choices: Choice) -> None:
        for choice in choices:
            self.choices.append(choice)

    def vote_for_choice(self, choice_text: str) -> None:
        for choice in self.choices:
            if choice.choice_text == choice_text:
                choice.votes += 1


class Choice:
    def __init__(self, id_: int | None, choice_text: str, votes: int):
        self.id = id_
        self.choice_text = choice_text
        self.votes = votes


class QuestionRepository:
    def add(self, *question: Question) -> None:
        raise NotImplementedError()

    def get(self, id_: int) -> Question | None:
        raise NotImplementedError()

    def get_all(self) -> list[Question]:
        raise NotImplementedError()

    def update(self, question: Question) -> None:
        raise NotImplementedError()

    def clear(self) -> None:
        raise NotImplementedError()
