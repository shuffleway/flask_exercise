
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Optional





class PostForm(FlaskForm):
    """Form for adding snack"""

    title = StringField("Title", validators=[InputRequired()])
    content = FloatField("Price in USD")



