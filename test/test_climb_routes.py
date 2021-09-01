"""User View Route."""
import os
from unittest import TestCase
from app import app

os.environ['DATABASE_URL'] = "postgresql:///climb-at-test"

app.config['WTF_CSRF_ENABLED'] = False

class TestClimbViews(TestCase):
    """Test Climb Views."""

    def setUp(self):
        """Create test client"""
        self.client = app.test_client()


    def tearDown(self):
        resp = super().tearDown()
        return resp

######################
# Tests Climb Views #
######################

    def test_climb_profile(self):
        with self.client as c:
            resp = c.get(f"climb/107506694")
            self.assertEqual(resp.status_code, 200)

            self.assertIn("Hroom", str(resp.data))

    def test_bad_climb_id(self):
        with self.client as c:
            resp = c.get(f"climb/107")
            self.assertEqual(resp.status_code, 302)

            resp = c.get(f"/landing")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("find climbs with the id of", str(resp.data))

    def test_sector_profile(self):
            with self.client as c:
                resp = c.get(f"climb/sector/107503567")
                self.assertEqual(resp.status_code, 200)

                self.assertIn("Broken Moon Boulder", str(resp.data))

                
    def test_bad_sector(self):
            with self.client as c:
                resp = c.get(f"climb/sector/107")
                self.assertEqual(resp.status_code, 302)
                
                resp = c.get(f"/search")
                self.assertEqual(resp.status_code, 200)
                self.assertIn("t find Crags with the id of 107", str(resp.data))
