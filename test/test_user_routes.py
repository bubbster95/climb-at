"""User View Route."""
import os
from unittest import TestCase
from models import db, connect_db, User, Completed, ToDo

os.environ['DATABASE_URL'] = "postgresql:///climb-at-test"

from app import app, CURR_USER_KEY 

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

####################
# Tests User Views #
####################

    def test_user_show(self):
        with self.client as c:
            resp = c.get(f"/user/{self.testuser_id}")
            self.assertEqual(resp.status_code, 200)

            self.assertIn("testuser", str(resp.data))

    def setup_completed(self):
        c1 = Completed(climb_id=117994489, climber_who_completed=self.testuser_id)

        db.session.add(c1)
        db.session.commit()
      

    def test_user_completed(self):
        self.setup_completed()

        with self.client as c:
            resp = c.get(f"/user/{self.testuser_id}")
            
            self.assertEqual(resp.status_code, 200)

            self.assertIn("Completed Climbs:", str(resp.data))

    def setup_todo(self):
        c2 = ToDo(climb_id=117994489, climber_to_do_it=self.testuser_id)

        db.session.add(c2)
        db.session.commit()
      

    def test_user_todo(self):
        self.setup_todo()

        with self.client as c:
            resp = c.get(f"/user/{self.testuser_id}")
            
            self.assertEqual(resp.status_code, 200)
            
            self.assertIn("Climbs To-Do:", str(resp.data))