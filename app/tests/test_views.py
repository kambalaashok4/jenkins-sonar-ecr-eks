"""Tests for views defined in app/views.py."""

from django.test import TestCase, Client
from django.urls import reverse


class LinkedinViewTests(TestCase):
    """Tests for linkedin_view."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("linkedin")
        # Cache the response so all tests reuse a single HTTP round-trip.
        self.response = self.client.get(self.url)

    # ------------------------------------------------------------------
    # Status code
    # ------------------------------------------------------------------

    def test_get_returns_200(self):
        """A GET request to '/' should return HTTP 200 OK."""
        self.assertEqual(self.response.status_code, 200)

    # ------------------------------------------------------------------
    # Template
    # ------------------------------------------------------------------

    def test_uses_correct_template(self):
        """The view should render profile/linkedin.html."""
        self.assertTemplateUsed(self.response, "profile/linkedin.html")

    # ------------------------------------------------------------------
    # Context variables
    # ------------------------------------------------------------------

    def test_context_contains_linkedin_url(self):
        """The template context must include the 'linkedin_url' key."""
        self.assertIn("linkedin_url", self.response.context)

    def test_linkedin_url_is_non_empty_string(self):
        """The linkedin_url context value should be a non-empty, non-whitespace string."""
        linkedin_url = self.response.context["linkedin_url"]
        self.assertIsInstance(linkedin_url, str)
        self.assertGreater(len(linkedin_url.strip()), 0)

    def test_linkedin_url_is_valid_https_link(self):
        """The linkedin_url context value should start with 'https://'."""
        linkedin_url = self.response.context["linkedin_url"]
        self.assertTrue(linkedin_url.startswith("https://"))

    # ------------------------------------------------------------------
    # Rendered content
    # ------------------------------------------------------------------

    def test_response_contains_linkedin_url_in_body(self):
        """The rendered HTML should include the linkedin URL as a hyperlink."""
        linkedin_url = self.response.context["linkedin_url"]
        self.assertContains(self.response, linkedin_url)
