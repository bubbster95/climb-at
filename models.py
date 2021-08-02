"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Completed(db.Model):
    """Connection of a climb <-> climber who did it."""

    __tablename__ = 'completed'

    completed_climb = db.Column(
        db.Integer,
        primary_key=True
    )

    climber_who_completed = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True
    )

class ToDo(db.Model):
    """Connection of a climb to do <-> climber to do it."""

    __tablename__ = 'todo'

    climb_to_do = db.Column(
        db.Integer,
        primary_key=True
    )

    climber_to_do_it = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True
    )


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    image_url = db.Column(
        db.Text,
        default="https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg?auto=compress&cs=tinysrgb&h=65&w=94"
    )

    bio = db.Column(
        db.Text
    )

    location = db.Column(
        db.Text
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    completed = db.relationship(
        "User",
        secondary="completed",
        primaryjoin=(Completed.climber_who_completed == id),
        secondaryjoin=(Completed.completed_climb == id)
    )

    todo = db.relationship(
        "User",
        secondary="todo",
        primaryjoin=(ToDo.climber_to_do_it == id),
        secondaryjoin=(ToDo.climb_to_do == id)
    )


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def is_climb_complete(self, this_climb):
        """Is this user followed by `other_user`?"""

        completed_climb_list = [climb for climb in self.completed if climb == this_climb]
        return len(completed_climb_list) == 1
   
    def is_climb_to_do(self, this_climb):
        """Is this user followed by `other_user`?"""

        climb_to_do_list = [climb for climb in self.todo if climb == this_climb]
        return len(climb_to_do_list) == 1

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )
        print("********** Testing ***********")
        print(user)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
