from store_app import db, login_manager, app
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(24), index=True)
    lastname = db.Column(db.String(24), index=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String)
    phonenumber = db.Column(db.String(18), index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    # user and order relationship is a one to many
    # order = db.relationship("Order", backref='ordered_products')

    # user and kart is one to one relationship
    # kart = db.relationship('Kart', uselist=False, backref='user_kart')
    # one to many relationships with Shipping info
    # change role
    # shipping_info = db.relationship('ShippingInfo', backref='shipping', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_secs=600):
        s = serializer(app.config['SECRET_KEY'], expires_secs)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return '<User {}>'.format(self.email)


@login_manager.user_loader
def load_user(_id):
    return User.query.get(int(_id))


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)
    img_file_name = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Good %r>' % self.name


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(JSON, nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.id


class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    good_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Order_detail %r>' % self.id
