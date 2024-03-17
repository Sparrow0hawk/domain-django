import os
from typing import Generator, Any

import django.conf
import pytest
from playwright.sync_api import BrowserContext
from pytest_django.live_server_helper import LiveServer

from tests.e2e.client import AppClient

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture(name="context")
def browser_context_fixture(
    context: BrowserContext,
) -> Generator[BrowserContext, None, None]:
    context.set_default_timeout(5_000)
    yield context


@pytest.fixture(name="settings_fixture", autouse=True)
def settings(settings: django.conf.LazySettings) -> None:
    settings.DEBUG_PROPAGATE_EXCEPTIONS = True
    settings.API_KEY = "marmite"


@pytest.fixture(name="app_client")
def app_client_fixture(live_server: LiveServer) -> Generator[AppClient, Any, Any]:
    app_client = AppClient(live_server.url, api_key="marmite")
    yield app_client
    app_client.clear_questions()
