import os
from typing import Generator

import pytest
from playwright.sync_api import BrowserContext

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture(name="context")
def browser_context_fixture(
    context: BrowserContext,
) -> Generator[BrowserContext, None, None]:
    context.set_default_timeout(5_000)
    yield context
