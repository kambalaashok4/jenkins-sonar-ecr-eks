"""Tests for views defined in app/views.py."""

from django.test import TestCase, Client
from django.urls import reverse


class LinkedinViewTests(TestCase):
    """Tests for linkedin_view."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("linkedin")

    # ------------------------------------------------------------------
    # Status code
    # ------------------------------------------------------------------

    def test_get_returns_200(self):
        """A GET request to '/' should return HTTP 200 OK."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # ------------------------------------------------------------------
    # Template
    # ------------------------------------------------------------------

    def test_uses_correct_template(self):
        """The view should render profile/linkedin.html."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "profile/linkedin.html")

    # ------------------------------------------------------------------
    # Context variables
    # ------------------------------------------------------------------

    def test_context_contains_linkedin_url(self):
        """The template context must include the 'linkedin_url' key."""
        response = self.client.get(self.url)
        self.assertIn("linkedin_url", response.context)

    def test_linkedin_url_is_non_empty_string(self):
        """The linkedin_url context value should be a non-empty string."""
        response = self.client.get(self.url)
        linkedin_url = response.context["linkedin_url"]
        self.assertIsInstance(linkedin_url, str)
        self.assertTrue(linkedin_url.strip())

    def test_linkedin_url_is_valid_https_link(self):
        """The linkedin_url context value should start with 'https://'."""
        response = self.client.get(self.url)
        linkedin_url = response.context["linkedin_url"]
        self.assertTrue(linkedin_url.startswith("https://"))

    # ------------------------------------------------------------------
    # Rendered content
    # ------------------------------------------------------------------

    def test_response_contains_linkedin_url_in_body(self):
        """The rendered HTML should include the linkedin URL as a hyperlink."""
        response = self.client.get(self.url)
        linkedin_url = response.context["linkedin_url"]
        self.assertContains(response, linkedin_url)
