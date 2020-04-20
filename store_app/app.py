import os
from flask import Flask, render_template
from store_app.models import db, User, Goods


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

    @app.route('/goods/<int:good_id>')
    def good(good_id: int):
        return render_template('good_template.html', good=Goods.query.filter_by(id=good_id).one())

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROJECT_ROOT'] = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    db.init_app(app)
