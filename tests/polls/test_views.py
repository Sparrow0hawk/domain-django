from django.test import TestCase
from django.urls import reverse


class TestPolls(TestCase):
    def test_index_shows_header(self) -> None:
        url = reverse("index")
        response = self.client.get(url)

        self.assertContains(response, "<h1>Hello world!</h1>")
