
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField, DecimalField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class EditUserForm(FlaskForm):
    """Form for editing users"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    bio = TextAreaField('Bio', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


def check_for_long(self, field):
    if not self.long.data:
        raise ValidationError("Must add Longitude to use Latittude")
def check_for_lat(self, field):
    if not self.lat.data:
        raise ValidationError("Must add Longitude to use Latittude")
def check_for_long_lat(self, field):
    if not self.long.data or not self.lat.data:
        raise ValidationError("Must add Longitude and Latittude to use radious")

class SearchForClimbsForm(FlaskForm):
    """Provides various filter options to search for climbs"""

    name = StringField("Climb Name", validators=[Optional(), Length(min=3)])
    fa = StringField("FA (First Ascent)", validators=[Optional()])
    lat = DecimalField("Latitude", places=10, validators=[Optional(), NumberRange(min=-90, max=90, message="This number must be between -90 and 90"), check_for_long])
    long = DecimalField("Longitude", places=10, validators=[Optional(), NumberRange(min=-180, max=180, message="This number must be between -180 and 180"), check_for_lat])
    radius = DecimalField("Radius", places=0, validators=[Optional()])
