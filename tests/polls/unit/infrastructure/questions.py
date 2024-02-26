import pytest

from polls.domain.questions import Question
from polls.infrastructure.questions import DatabaseQuestionRepository
from polls.models import QuestionEntity


@pytest.fixture(name="questions_repository")
def questions_fixture() -> DatabaseQuestionRepository:
    return DatabaseQuestionRepository()


@pytest.mark.django_db(transaction=True)
class TestDatabaseQuestionRepository:
    def test_add_question(self, questions_repository: DatabaseQuestionRepository) -> None:
        questions_repository.add(Question(id_=1, question_text="Who are you?"))

        question1 = QuestionEntity.objects.filter(pk=1).get()
        assert question1 and question1.id == 1 and question1.question_text == "Who are you?"

    def test_get_question(self, questions_repository: DatabaseQuestionRepository) -> None:
        question = QuestionEntity(id=1, question_text="Who are you?")
        question.save()

        question1 = questions_repository.get(1)
        assert question1 and question1.id == 1 and question1.question_text == "Who are you?"
