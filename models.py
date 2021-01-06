from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'
        self.id = 0


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), nullable=False) 
    password_hash = db.Column(db.String(100), nullable=False)
    # __table_args__ = {'extend_existing': True}

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


order_product = db.Table('order_product',
                         db.Column('order_id', db.Integer, db.ForeignKey('order.order_id'), primary_key=True),
                         db.Column('product_id', db.Integer, db.ForeignKey('Product.id'), primary_key=True),
                         extend_existing = True
                         )


class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    picture_path = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(10), nullable=True)
    size = db.Column(db.String(10), nullable=True)
    __table_args__ = {'extend_existing': True}


class Cart_product(db.Model):
    __tablename__ = 'cart_product'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'Product.id'), primary_key=True)
    number = db.Column(db.Integer, default=1)
    user = db.relation('User', backref=db.backref('cart_products'))
    product = db.relation('Product', backref=db.backref('cart_products'))
    __table_args__ = {'extend_existing': True}


class Profile(db.Model):
    __tablename__ = 'profile'
    profile_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), primary_key=True)
    first_Name = db.Column(db.String(20), nullable=False)
    last_Name = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(50), nullable=True)
    photo_path = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=True)
    telephone = db.Column(db.String(20), nullable=False)
    fax = db.Column(db.String(30), nullable=True)
    user = db.relation('User', backref=db.backref('profile'))
    __table_args__ = {'extend_existing': True}


class Address(db.Model):
    __tablename__ = 'address'
    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    province = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    postcode = db.Column(db.String(20), nullable=False)
    default_address = db.Column(db.Boolean, nullable=True)
    user = db.relation('User', backref=db.backref('addresses'))
    __table_args__ = {'extend_existing': True}


class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'))
    product = db.relation('Product', backref=db.backref('product'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relation('User', backref=db.backref('reviews'))
    content = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=False, default=3)
    create_time = db.Column(db.DateTime, default=datetime.now)
    __table_args__ = {'extend_existing': True}


class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_price = db.Column(db.Integer)
    destination = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, default=datetime.now)
    user = db.relation('User', backref=db.backref('orders'))
    products = db.relationship('Product', secondary=order_product, backref=db.backref('orders'))
    __table_args__ = {'extend_existing': True}



