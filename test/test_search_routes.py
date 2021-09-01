"""User View Route."""
import os
from unittest import TestCase
from app import app

os.environ['DATABASE_URL'] = "postgresql:///climb-at-test"

app.config['WTF_CSRF_ENABLED'] = False

class TestSearchViews(TestCase):
    """Test Search Views."""

    def setUp(self):
        """Create test client"""
        self.client = app.test_client()


    def tearDown(self):
        resp = super().tearDown()
        return resp

######################
# Tests Search Views #
######################

    def test_search_view(self):
        with self.client as c:
            resp = c.get(f"/search")
            self.assertEqual(resp.status_code, 200)

            self.assertIn("Search For Crags", str(resp.data))

