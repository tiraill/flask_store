from flask_wtf import FlaskForm
from wtforms import SubmitField


class AddToCart(FlaskForm):
    # sizes = RadioField('Sizes',validators=[DataRequired(message="select a product size")],
    # choices=[('Small','S'),('Medium','M'),('Large','L'),('Extra Large','XL')])
    submit = SubmitField('Добавить в корзину')

