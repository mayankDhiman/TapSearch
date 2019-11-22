from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,IntegerField, TextAreaField
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.validators import Email,EqualTo,DataRequired
from wtforms import ValidationError
from flask_wtf.file import FileAllowed, FileField

class QueryForm(FlaskForm):
    query = StringField('Query', render_kw={"placeholder":"Your Queries Here!"})
    submit = SubmitField('Go!')


class NewDocForm(FlaskForm):
    document = TextAreaField('New Document', render_kw={"placeholder":"Enter new data here"})
    submit = SubmitField('Add')
