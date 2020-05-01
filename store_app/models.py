from store_app import db, login_manager, app
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from flask_login import UserMixin


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(24), index=True)
    lastname = db.Column(db.String(24), index=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String)
    phonenumber = db.Column(db.String(18), index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    # relationships
    # one to many relationships
    order = db.relationship('Order')
    # one to many relationship
    cart = db.relationship('Cart')
    # one to many relationships
    shipping_info = db.relationship('ShippingInfo')

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


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, index=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    product_price = db.Column(db.Integer, index=True, nullable=False)
    product_stock = db.Column(db.Integer, nullable=False)
    product_description = db.Column(db.String, nullable=True)
    img_file_name = db.Column(db.String, nullable=True)
    properties = db.Column(db.JSON)

    def __repr__(self):
        return '<Product %r>' % self.product_name


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, index=True, nullable=False)

    # relationships
    # one to many relationships
    product = db.relationship('Products', backref='product_category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.category_name

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=True)

    # relationships
    status = db.relationship('OrderStatus')
    order_detail = db.relationship('OrderDetail')

    def __repr__(self):
        return '<Order %r>' % self.id


class OrderDetail(db.Model):
    __tablename__ = 'order_detail'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Order detail %r>' % self.id


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Cart %r>' % self.id


class ShippingInfo(db.Model):
    __tablename__ = 'shipping_info'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    country = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Shipping Info %r>' % self.id


class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    status = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<OrderStatus %r>' % self.id