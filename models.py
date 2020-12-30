from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'
        self.id = 0

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(20), nullable = False)
    username = db.Column(db.String(50),nullable=False)
    password_hash = db.Column(db.String(100),nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80),nullable=False)
    picture_path = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(10), nullable=True)
    size = db.Column(db.String(10), nullable=True)


class Cart_product(db.Model):
    __tablename__ = 'cart_product'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), primary_key=True)
    number = db.Column(db.Integer, default=1)
    user = db.relation('User', backref=db.backref('cart_products'))
    product = db.relation('Product', backref=db.backref('cart_products'))