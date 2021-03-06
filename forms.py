
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, IntegerField
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
    password = PasswordField('Password', validators=[Length(min=6)])
    bio = TextAreaField('Bio', validators=[DataRequired()])

def check_for_long(self, field):
    if not self.lng.data:
        raise ValidationError("Must add Longitude to use Latittude")
        
def check_for_lat(self, field):
    if not self.lat.data:
        raise ValidationError("Must add Longitude to use Latittude")

def check_for_long_lat(self, field):
    if not self.lng.data or not self.lat.data:
        raise ValidationError("Must add Longitude and Latittude to use radious")

class SearchByCoordinate(FlaskForm):
    """Allows users to search for sectors near their Longitude and Latittude."""
    
    lat = DecimalField("Latitude", places=10, validators=[Optional(), NumberRange(min=-90, max=90, message="This number must be between -90 and 90"), check_for_long])
    lng = DecimalField("Longitude", places=10, validators=[Optional(), NumberRange(min=-180, max=180, message="This number must be between -180 and 180"), check_for_lat])
    radius = DecimalField("Radius (Km)", places=0, validators=[Optional()])


class SearchByAddress(FlaskForm):
    """Lets users find coordinates by filling in an adress"""

    number = IntegerField("Number: 400")
    street = StringField("Street: climber street")
    town = StringField("Town: boulder")
    state = StringField("State: colorado")
    radius = DecimalField("Radius (Km)", places=0, validators=[Optional()])


