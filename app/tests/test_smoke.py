"""Smoke tests for ASGI and WSGI application callables."""

from django.test import SimpleTestCase


class WsgiSmokeTest(SimpleTestCase):
    """Verify that the WSGI application can be imported and is callable."""

    def test_wsgi_application_is_callable(self):
        """app.wsgi.application must exist and be callable."""
        from app.wsgi import application  # noqa: PLC0415

        self.assertTrue(callable(application))


class AsgiSmokeTest(SimpleTestCase):
    """Verify that the ASGI application can be imported and is callable."""

    def test_asgi_application_is_callable(self):
        """app.asgi.application must exist and be callable."""
        from app.asgi import application  # noqa: PLC0415

        self.assertTrue(callable(application))
