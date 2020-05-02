from store_app import app, db
from flask import (
    render_template, Blueprint,
    request, redirect, url_for, session, flash, abort
)
from flask_login import current_user, login_required

from store_app.utils import AddToCart
from store_app.models import Products, Cart
from sqlalchemy.sql import exists
# from app.admin.forms import Variations
# import random
store = Blueprint('store', __name__)


@store.route('/')
def landing():
    return render_template(
        'index.html',
        count=cart_count()
    )


@store.route('/products', methods=["GET", "POST"])
def products():
    form = AddToCart()

    if form.validate_on_submit():
        if add_to_cart(form.product_id.data, form.product_price.data):
            flash("{} has been added to cart".format(form.product_name.data))
            return redirect(url_for('store.products'))
        else:
            flash('please login before you can add items to your shopping cart', 'warning')
            return redirect(url_for('store.products'))

    return render_template(
        'products.html',
        form=form,
        count=cart_count(),
        products=Products.query.all()
    )


@store.route('/product/<int:product_id>', methods=["GET", "POST"])
def product(product_id: int):
    form = AddToCart()
    if form.validate_on_submit():
        if add_to_cart(form.product_id.data, form.product_price.data):
            flash("{} has been added to cart".format(form.product_name.data))
            return redirect(url_for('store.product', product_id=product_id))
        else:
            flash('please login before you can add items to your shopping cart', 'warning')
            return redirect(url_for("store.product", product_id=product_id))

    return render_template(
        'product_template.html',
        form=form,
        count=cart_count(),
        product=Products.query.filter_by(id=product_id).one()
    )


def add_to_cart(product_id, product_price) -> bool:
    if current_user.is_anonymous:
        return False

    if db.session.query(
            Cart.query.filter_by(
                user_id=current_user.id,
                product_id=product_id
            ).exists()).scalar():
        return True
    else:
        cart = Cart(user_id=current_user.id, product_id=product_id, quantity=1, subtotal=product_price)
        db.session.add(cart)
        db.session.commit()
        return True


def cart_count() -> int:
    if current_user.is_anonymous:
        count = 0
    else:
        count = Cart.query.filter_by(user_id=current_user.id).count()
    return count
