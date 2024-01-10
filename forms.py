from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired

class Notebook(FlaskForm):
    name = StringField(
        'Notebook Name',
        validators=[
                DataRequired(),
                Length(min=10, max=500)
            ]
        )
    description = TextAreaField(
        'Description',
        validators=[
            DataRequired()
        ]
    )