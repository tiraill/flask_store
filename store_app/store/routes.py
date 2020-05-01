# from store_app import app, db
from flask import (
    render_template, Blueprint,
    # request, redirect, url_for, session, flash, abort
)
# from flask_login import current_user, login_required

# from app.models import User, Categories, Products,Kart
from store_app.models import Products
# from app.admin.forms import Variations
# import random
store = Blueprint('store', __name__)


@store.route('/')
def landing():
    return render_template('index.html')


@store.route('/goods')
def goods():
    return render_template('goods.html', goods_list=Products.query.all())


@store.route('/goods/<int:good_id>', methods=["GET", "POST"])
def good(good_id: int):
    # form = AddToCart()
    #
    # if form.validate_on_submit():
    #     cur_user_id = 1
    #     order = Orders(user_id=cur_user_id, price=0, status='{}')
    #     db.session.add(order)
    #     db.session.commit()
    #
    #     detail = Order_detail(order_id=order.id, good_id=good_id, quantity=1)
    #     db.session.add(detail)
    #     db.session.commit()
    #     return render_template('goods.html', goods_list=Goods.query.all())

    return render_template(
        'good_template.html',
        good=Products.query.filter_by(id=good_id).one()
    )
