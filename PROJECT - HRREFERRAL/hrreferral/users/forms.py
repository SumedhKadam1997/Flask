from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired,Email ,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from hrreferral.models import Users


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

class ReferralForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    designation = StringField('Designation',validators=[DataRequired()])
    exp = IntegerField('Years of Experience',validators=[DataRequired()])
    comp_name = StringField('Company Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChangePassForm(FlaskForm):
    current_pass = PasswordField('Current Password',validators=[DataRequired()])
    new_pass =PasswordField('New Password',validators=[DataRequired(), EqualTo('new_pass_confirm',message='New Passwords must match')])
    new_pass_confirm = PasswordField('Confirm New Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('String')
    submit = SubmitField('Search')
