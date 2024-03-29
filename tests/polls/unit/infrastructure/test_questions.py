import pytest

from polls.domain.questions import Question, Choice
from polls.infrastructure.questions import DatabaseQuestionRepository
from polls.models import QuestionEntity, ChoiceEntity


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

    def test_add_questions_saves_choices(self, questions_repository: DatabaseQuestionRepository) -> None:
        question = Question(id_=1, question_text="Who are you?")
        question.add_choices(Choice(id_=2, choice_text="John Smith", votes=1))
        questions_repository.add(question)

        question_entity = QuestionEntity.objects.get(pk=1)
        assert question_entity.id == 1
        choice1: ChoiceEntity
        (choice1,) = question_entity.choiceentity_set.all()
        assert choice1.id == 2 and choice1.choice_text == "John Smith" and choice1.votes == 1

    def test_get_question(self, questions_repository: DatabaseQuestionRepository) -> None:
        question_entity = QuestionEntity(id=1, question_text="Who are you?")
        question_entity.save()
        choice_entity = ChoiceEntity(id=2, choice_text="John Smith", question=question_entity)
        choice_entity.save()

        question1 = questions_repository.get(1)
        assert question1 and question1.id == 1 and question1.question_text == "Who are you?"
        (choice1,) = question1.choices
        assert choice1.id == 2 and choice1.choice_text == "John Smith"

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

    def test_get_all_questions_gets_choices(self, questions_repository: DatabaseQuestionRepository) -> None:
        question_entity1 = QuestionEntity(id=1, question_text="Who are you?")
        question_entity2 = QuestionEntity(id=2, question_text="What is your favourite sandwich?")
        question_entity1.save()
        question_entity2.save()

        ChoiceEntity(id=3, choice_text="John Smith", votes=0, question=question_entity1).save()

        question1: Question
        question2: Question
        question1, question2 = questions_repository.get_all()
        assert (
            question1.id == 1
            and question1.question_text == "Who are you?"
            and question2.id == 2
            and question2.question_text == "What is your favourite sandwich?"
        )
        choice1: Choice
        (choice1,) = question1.choices
        assert choice1.id == 3 and choice1.choice_text == "John Smith" and choice1.votes == 0 and not question2.choices

    def test_update_questions_saves_vote(self, questions_repository: DatabaseQuestionRepository) -> None:
        question_entity = QuestionEntity(id=1, question_text="Who are you?")
        question_entity.save()
        ChoiceEntity(id=3, choice_text="John Smith", votes=0, question=question_entity).save()
        ChoiceEntity(id=4, choice_text="Ringo Starr", votes=0, question=question_entity).save()

        question = questions_repository.get(1)
        assert question
        question.vote_for_choice("Ringo Starr")
        questions_repository.update(question)

        question1 = QuestionEntity.objects.get(pk=1)
        assert question1.id == 1 and question1.question_text == "Who are you?"
        choice_entity1: ChoiceEntity
        choice_entity2: ChoiceEntity
        (choice_entity1, choice_entity2) = question1.choiceentity_set.all()
        assert (
            choice_entity1.choice_text == "John Smith"
            and choice_entity1.votes == 0
            and choice_entity2.choice_text == "Ringo Starr"
            and choice_entity2.votes == 1
        )

    def test_clear_questions(self, questions_repository: DatabaseQuestionRepository) -> None:
        question_entity = QuestionEntity(id=1, question_text="Who are you?")
        question_entity.save()

        questions_repository.clear()

        assert not questions_repository.get_all()
