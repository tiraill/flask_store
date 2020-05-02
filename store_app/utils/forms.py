from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField


class AddToCart(FlaskForm):
    product_id = HiddenField('id')
    product_price = HiddenField('price')
    product_name = HiddenField('name')
    submit = SubmitField('Добавить в корзину')

