from playwright.sync_api import Page
from pytest_django.live_server_helper import LiveServer


def test_index_shows_header(live_server: LiveServer, page: Page) -> None:
    page.goto(live_server.url)

    index_heading = page.get_by_role("heading")

    assert index_heading.text_content() == "Hello world!"
