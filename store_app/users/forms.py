from flask_wtf import FlaskForm
from wtforms import(StringField,IntegerField, PasswordField,
SubmitField, validators, SelectField)

from wtforms.validators import ValidationError, DataRequired, Email

# from app.models import User

from flask_login import current_user


class CartForm(FlaskForm):
    quantity = IntegerField('1', validators=[DataRequired()])
    submit = SubmitField('Submit')
