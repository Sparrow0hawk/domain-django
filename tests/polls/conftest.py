import inject
import pytest
from inject import Binder

from polls.domain.questions import QuestionRepository
from tests.polls.fakes import MemoryQuestionRepository


@pytest.fixture(name="config")
def config_fixture() -> None:
    inject.clear_and_configure(_bindings)
    yield
    inject.clear()


@pytest.fixture(name="questions")
def questions_fixture() -> QuestionRepository:
    questions: QuestionRepository = inject.instance(QuestionRepository)
    yield questions


def _bindings(binder: Binder) -> None:
    binder.bind(QuestionRepository, MemoryQuestionRepository())
