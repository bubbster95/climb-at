"""User model tests."""
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

# Set eviron variable for tests
os.environ['DATABASE_URL'] = "postgresql:///climb-at-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for User"""

    def setUp(self):
        """Create test user and sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email@email.com", "password", None)
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "password", None)
        uid2 = 2222
        u2.id = uid2 

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.completed), 0)
        self.assertEqual(len(u.todo), 0)

    
    ################
    # Signup Tests #
    ################

    def test_valid_signup(self):
        u_test = User.signup("FuzzyWuzzy", "wazaBear@gmail.com", 'password', None)
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, 'FuzzyWuzzy')
        self.assertEqual(u_test.email, "wazaBear@gmail.com")
        self.assertNotEqual(u_test.password, 'password')
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, 'test@test.com', 'password', None)
        uid = 12345
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("testtest", None, "password", None)
        uid = 134567
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup('testtest', "email@email.com", '', None)

        with self.assertRaises(ValueError) as context:
            User.signup('testtest', 'email@email.com', None, None)
    
    #######################
    # Authentication Test #
    #######################

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, 'password')
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate('badusername', "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, 'badpassword'))
