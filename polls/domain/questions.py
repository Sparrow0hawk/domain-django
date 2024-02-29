class Question:
    def __init__(self, id_: int, question_text: str):
        self.id = id_
        self.question_text = question_text


class QuestionRepository:
    def add(self, *question: Question) -> None:
        raise NotImplementedError()

    def get(self, id_: int) -> Question | None:
        raise NotImplementedError()
