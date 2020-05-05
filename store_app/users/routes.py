from store_app import app
from flask import (
    render_template, request, redirect, url_for, session,
    flash, Blueprint,
    jsonify)

from store_app.models import db, Users, Cart
import gc
from store_app.users.forms import CartForm, ProfileForm
from store_app.auth.forms import RegistrationForm, LoginForm
from flask_login import (
    current_user, login_user, logout_user, login_required
)

users = Blueprint('users', __name__)


def ShippingPrice():
    '''
    calculate the price of shipping if items is greater than 5 shipping is 2500
    else 1200
    '''
    if current_user.is_authenticated:
        # check this otherwise revert to
        # item_num = Kart.query.filter_by(user_id = Kart.user_id).count()
        item_num = Cart.query.filter_by(user_id=current_user.id).count()
    else:
        item_num = Cart.query.filter_by(user_id=0).count()

    shipping_price = 0
    if item_num >= 1:
        shipping_price = 1200
    elif item_num >= 5:
        shipping_price = 2500
    else:
        pass
    return shipping_price


def subtotals():
    if current_user.is_authenticated:
        # check this otherwise revert to
        # item_num = Kart.query.filter_by(user_id = Kart.user_id).count()
        get_products = Cart.query.filter_by(user_id=current_user.id).all()
    else:
        get_products = Cart.query.filter_by(user_id=0).all()

    items_subtotal = 0
    # get_products = Kart.query.filter_by(user_id = Kart.user_id).all()

    for price in get_products:
        items_subtotal += int(price.subtotal)
    return items_subtotal


@users.route('/cart/', methods=["GET", "POST"])
def cart():
    if current_user.is_anonymous:
        count = 0
        user = 0
        cartlist = []
    else:
        user = current_user.id
        count = Cart.query.filter_by(user_id =user).count()
        cartlist = Cart.query.filter_by(user_id=user).all()

    form = CartForm()
    # fetch cart data

    # shipping = ShippingInfo.query.all()
    price = ShippingPrice()
    items_subtotals = subtotals()
#     # for annoymous users
#     if current_user.is_anonymous:
#         flash('please login or register to be able to add a shipping address')
#         return render_template('users/cart.html', count= count, cartlist= cartlist,
#                                title = "Cart", form = form, price=price, items_subtotals=items_subtotals)
#
    return render_template(
        'users/cart.html',
        count=count,
        cartlist=cartlist,
        title="Cart",
        form=form,
        price=price,
        items_subtotals=items_subtotals
    )


@users.route('/cart/update/<int:id>', methods=["POST"])
def quantity_update(id):
    cart_item = Cart.query.get_or_404(id)
    quantity = request.form["quantity"]
    cart_item.quantity = quantity
    item_total = cart_item.product.product_price * int(quantity)
    cart_item.subtotal = item_total
    items_subtotal = subtotals()
    db.session.commit()
    gc.collect()
    return jsonify({"result": "success", "item_total": item_total, "subtotal": items_subtotal})


@users.route('/cart/remove/<int:id>', methods=["GET", "POST"])
def remove_item(id):
    cart_item = Cart.query.get_or_404(id)
    db.session.delete(cart_item)
    db.session.commit()
    gc.collect()
    return redirect(url_for('users.cart'))


@users.route('/profile/', methods=["GET", "POST"])
def profile():

    profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        user: Users = Users.query.filter_by(id=current_user.id).one()
        user.firstname = profile_form.firstname.data
        user.lastname = profile_form.lastname.data
        user.email = profile_form.email.data
        user.phonenumber = profile_form.phonenumber.data

        db.session.commit()
        gc.collect()
        flash('shipping information was submitted successfully', 'success')
        return redirect(url_for('users.profile'))
    return render_template(
        'users/profile.html',
        profile_form=profile_form
    )
