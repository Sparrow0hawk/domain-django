from typing import Generator, Any

from polls.domain.questions import Question, QuestionRepository, Choice
from polls.models import QuestionEntity, ChoiceEntity


class DatabaseQuestionRepository(QuestionRepository):
    def add(self, *questions: Question) -> None:
        for question in questions:
            question_entity = self._domain_to_entity(question)
            question_entity.save()

            for choice in question.choices:
                choice_entity = self._choice_map_to_entity(choice, question_entity)
                choice_entity.save()

    def get(self, id_: int) -> Question | None:
        question_entity = QuestionEntity.objects.get(id=id_)
        question = self._entity_to_domain(question_entity)

        for choice_entity in question_entity.choiceentity_set.all():
            question.add_choices(self._choice_map_to_domain(choice_entity))

        return question

    def get_all(self) -> list[Question]:
        def get_all_generator() -> Generator[Question, Any, Any]:
            for question_entity in QuestionEntity.objects.all():
                question = self._entity_to_domain(question_entity)

                for choice_entity in question_entity.choiceentity_set.all():
                    question.add_choices(self._choice_map_to_domain(choice_entity))
                yield question

        return [question for question in get_all_generator()]

    def clear(self) -> None:
        QuestionEntity.objects.all().delete()

    @staticmethod
    def _entity_to_domain(question_entity: QuestionEntity) -> Question:
        return Question(id_=question_entity.id, question_text=question_entity.question_text)

    @staticmethod
    def _domain_to_entity(question: Question) -> QuestionEntity:
        return QuestionEntity(id=question.id, question_text=question.question_text)

    @staticmethod
    def _choice_map_to_domain(choice_entity: ChoiceEntity) -> Choice:
        return Choice(id_=choice_entity.id, choice_text=choice_entity.choice_text)

    @staticmethod
    def _choice_map_to_entity(choice: Choice, question_entity: QuestionEntity) -> ChoiceEntity:
        return ChoiceEntity(id=choice.id, choice_text=choice.choice_text, question=question_entity)
