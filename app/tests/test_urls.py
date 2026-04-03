"""Tests for URL configuration in app/urls.py."""

from django.test import TestCase
from django.urls import reverse, resolve

from app.views import linkedin_view


class UrlReverseTests(TestCase):
    """Verify that named URL patterns resolve to the expected paths."""

    def test_linkedin_url_reverses_to_root(self):
        """The 'linkedin' URL name should resolve to the site root '/'."""
        url = reverse("linkedin")
        self.assertEqual(url, "/")

    def test_root_url_resolves_to_linkedin_view(self):
        """A GET to '/' should be routed to linkedin_view."""
        resolver_match = resolve("/")
        self.assertEqual(resolver_match.func, linkedin_view)

    def test_root_url_pattern_name(self):
        """The URL pattern for '/' should carry the name 'linkedin'."""
        resolver_match = resolve("/")
        self.assertEqual(resolver_match.url_name, "linkedin")
