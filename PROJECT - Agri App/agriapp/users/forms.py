from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, FloatField
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import DataRequired,Email ,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from agriapp.models import Users


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

class CropForm(FlaskForm):
    crop_name = StringField('Crop Name', validators=[DataRequired()])
    date_planted = DateField('Date Planted', format = "%Y-%m-%d", validators=[DataRequired()])
    area = IntegerField('Area', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FertilizerForm(FlaskForm):
    date_of_apply = DateField('Date of Application', format = "%Y-%m-%d",validators=[DataRequired()])
    urea = IntegerField('Urea',validators=[DataRequired()])
    dap = IntegerField('DAP', validators=[DataRequired()])
    ammonium_sulphate = IntegerField('Ammonium Sulphate', validators=[DataRequired()])
    bag_of_12X32X16 = IntegerField('bag_of_12X32X16', validators=[DataRequired()])
    bag_of_10X26X26 = IntegerField('bag_of_10X26X26', validators=[DataRequired()])
    mop = IntegerField('MOP', validators=[DataRequired()])
    micronutrients = IntegerField('Micro Nutrients', validators=[DataRequired()])
    sulphur = IntegerField('Sulphur', validators=[DataRequired()])
    bag_of_19X19X19 = IntegerField('bag_of_19X19X19', validators=[DataRequired()])
    bag_of_20X20X0X13 = IntegerField('bag_of_20X20X0X13', validators=[DataRequired()])
    cost = IntegerField('Cost', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')

class WaterSolubleFertForm(FlaskForm):
    date_of_apply = DateField('Date of Application', format='%Y-%m-%d',validators=[DataRequired()])
    bag_of_19X19X19 = IntegerField('bag_of_19X19X19', validators=[DataRequired()])
    bag_of_13X40X13 = IntegerField('bag_of_13X40X13', validators=[DataRequired()])
    bag_of_13X0X45 = IntegerField('bag_of_13X0X45', validators=[DataRequired()])
    bag_of_0X52X34 = IntegerField('bag_of_0X52X34', validators=[DataRequired()])
    bag_of_12X61X0 = IntegerField('bag_of_12X61X0', validators=[DataRequired()])
    calcium_nitrate = IntegerField('calcium_nitrate', validators=[DataRequired()])
    cost = IntegerField('Cost', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')

class ChangePassForm(FlaskForm):
    current_pass = PasswordField('Current Password',validators=[DataRequired()])
    new_pass =PasswordField('New Password',validators=[DataRequired(), EqualTo('new_pass_confirm',message='New Passwords must match')])
    new_pass_confirm = PasswordField('Confirm New Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('String')
    submit = SubmitField('Search')