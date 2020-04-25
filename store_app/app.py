import os
from flask import Flask, render_template, redirect
from store_app.models import db, User, Goods, Orders, Order_detail
from store_app.utils.forms import AddToCart


def create_app():
    """Returns an initialized Flask application."""
    app = Flask(__name__)
    register_extensions(app)

    @app.route('/')
    def hello_world():
        return render_template('index.html')

    @app.route('/users')
    def users():
        return render_template('users.html', user_list=User.query.all())

    @app.route('/goods')
    def goods():
        return render_template('goods.html', goods_list=Goods.query.all())

    @app.route('/goods/<int:good_id>', methods=["GET", "POST"])
    def good(good_id: int):
        form = AddToCart()

        if form.validate_on_submit():
            cur_user_id = 1
            order = Orders(user_id=cur_user_id, price=0, status='{}')
            db.session.add(order)
            db.session.commit()

            detail = Order_detail(order_id=order.id, good_id=good_id, quantity=1)
            db.session.add(detail)
            db.session.commit()
            return render_template('goods.html', goods_list=Goods.query.all())

        return render_template(
            'good_template.html',
            form=form,
            good=Goods.query.filter_by(id=good_id).one()
        )

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROJECT_ROOT'] = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)
