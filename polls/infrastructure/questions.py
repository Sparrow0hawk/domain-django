from polls.domain.questions import Question, QuestionRepository
from polls.models import QuestionEntity


class DatabaseQuestionRepository(QuestionRepository):
    def add(self, *questions: Question) -> None:
        for question in questions:
            question_entity = self._domain_to_entity(question)
            question_entity.save()

    def get(self, id_: int) -> Question | None:
        return self._entity_to_domain(QuestionEntity.objects.get(id=id_))

    def get_all(self) -> list[Question]:
        return [self._entity_to_domain(question) for question in QuestionEntity.objects.all()]

    @staticmethod
    def _entity_to_domain(question_entity: QuestionEntity) -> Question:
        return Question(id_=question_entity.id, question_text=question_entity.question_text)

    @staticmethod
    def _domain_to_entity(question: Question) -> QuestionEntity:
        return QuestionEntity(id=question.id, question_text=question.question_text)
