from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired,Email ,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from agriapp.models import Users


class ContactForm(FlaskForm):
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    subject = StringField('Subject',validators=[DataRequired()])
    message = TextAreaField('Message')
    submit = SubmitField('Submit')
    
class SearchForm(FlaskForm):
    search = StringField('Search')
    submit = SubmitField('Submit')