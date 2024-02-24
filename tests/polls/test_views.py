from django.test import Client
from django.urls import reverse


def test_index_shows_header(client: Client) -> None:
    url = reverse("index")
    response = client.get(url)

    assert b"<h1>Hello world!</h1>" == response.content
