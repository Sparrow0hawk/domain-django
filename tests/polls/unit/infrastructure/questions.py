import pytest

from polls.domain.questions import Question
from polls.infrastructure.questions import DatabaseQuestionRepository
from polls.models import QuestionEntity


@pytest.fixture(name="questions_repository")
def questions_fixture() -> DatabaseQuestionRepository:
    return DatabaseQuestionRepository()


@pytest.mark.django_db(transaction=True)
class TestDatabaseQuestionRepository:
    def test_add_questions(self, questions_repository: DatabaseQuestionRepository) -> None:
        questions_repository.add(
            Question(id_=1, question_text="Who are you?"),
            Question(id_=2, question_text="What is your favourite sandwich?"),
        )

        questions = QuestionEntity.objects.all()
        assert (
            questions[0]
            and questions[0].id == 1
            and questions[0].question_text == "Who are you?"
            and questions[1]
            and questions[1].id == 2
            and questions[1].question_text == "What is your favourite sandwich?"
        )

    def test_get_question(self, questions_repository: DatabaseQuestionRepository) -> None:
        question_entity = QuestionEntity(id=1, question_text="Who are you?")
        question_entity.save()

        question1 = questions_repository.get(1)
        assert question1 and question1.id == 1 and question1.question_text == "Who are you?"

    def test_get_all_questions(self, questions_repository: DatabaseQuestionRepository) -> None:
        question_entities = [
            QuestionEntity(id=1, question_text="Who are you?"),
            QuestionEntity(id=2, question_text="What is your favourite sandwich?"),
            QuestionEntity(id=3, question_text="What is your favourite colour?"),
        ]

        for item in question_entities:
            item.save()

        question1: Question
        question2: Question
        question3: Question
        question1, question2, question3 = questions_repository.get_all()

        assert (
            question1.id == 1
            and question1.question_text == "Who are you?"
            and question2.id == 2
            and question2.question_text == "What is your favourite sandwich?"
            and question3.id == 3
            and question3.question_text == "What is your favourite colour?"
        )
