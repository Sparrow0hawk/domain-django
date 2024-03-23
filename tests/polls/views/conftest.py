from typing import Generator

import inject
import pytest
from inject import Binder

from polls.domain.questions import QuestionRepository
from tests.polls.views.fakes import MemoryQuestionRepository


@pytest.fixture(name="config")
def config_fixture() -> Generator[None, None, None]:
    inject.clear_and_configure(_bindings)
    yield
    inject.clear()


@pytest.fixture(name="questions")
def questions_fixture() -> Generator[QuestionRepository, None, None]:
    questions: QuestionRepository = inject.instance(QuestionRepository)
    yield questions


def _bindings(binder: Binder) -> None:
    binder.bind(QuestionRepository, MemoryQuestionRepository())
