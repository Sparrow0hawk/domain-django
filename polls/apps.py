import inject
from django.apps import AppConfig
from inject import Binder

from polls.domain.questions import QuestionRepository


class PollsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "polls"

    def ready(self):
        from polls.infrastructure.questions import DatabaseQuestionRepository

        def _bindings(binder: Binder) -> None:
            binder.bind_to_constructor(QuestionRepository, DatabaseQuestionRepository)

        inject.configure(_bindings)
