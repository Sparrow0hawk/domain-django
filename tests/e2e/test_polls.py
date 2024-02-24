from playwright.sync_api import Page


def test_index_shows_header(live_server, page: Page):
    page.goto(live_server.url)

    index_heading = page.get_by_role("heading")

    assert index_heading.text_content() == "Hello world!"
