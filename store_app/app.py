import os
from flask import Flask, render_template
from store_app.models import db, User, Goods


def create_app():
    """Returns an initialized Flask application."""
    app = Flask(__name__)
    register_extensions(app)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/users')
    def users():
        return render_template('users.html', user_list=User.query.all())

    @app.route('/goods')
    def goods():
        return render_template('goods.html', goods_list=Goods.query.all())

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROJECT_ROOT'] = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    db.init_app(app)
