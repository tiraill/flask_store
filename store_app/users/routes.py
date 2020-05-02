from store_app import app
from flask import (
    render_template, request, redirect, url_for, session,
    flash, Blueprint
)

from store_app.models import db, Users
import gc
from store_app.auth.forms import RegistrationForm, LoginForm
from flask_login import (
    current_user, login_user, logout_user, login_required
)

users = Blueprint('users', __name__)

#
@users.route('/cart/', methods=["GET", "POST"])
def cart():
#     if current_user.is_anonymous:
#         count = 0
#         user = 0
#         cartlist = []
#     else:
#         user = current_user.id
#         count = Kart.query.filter_by(user_id =user).count()
#         cartlist = Kart.query.filter_by(user_id=user).all()
#
#     form = CartForm()
#     # fetch cart data
#
#     # shipping = ShippingInfo.query.all()
#     price = ShippingPrice()
#     items_subtotals = subtotals()
#     # for annoymous users
#     if current_user.is_anonymous:
#         flash('please login or register to be able to add a shipping address')
#         return render_template('users/cart.html', count= count, cartlist= cartlist,
#                                title = "Cart", form = form, price=price, items_subtotals=items_subtotals)
#
    return render_template('users/cart.html')