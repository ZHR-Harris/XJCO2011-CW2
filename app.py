from flask import Flask, render_template, request, url_for, redirect, session, g, flash
import config
from exts import db
from models import User, Product
import re
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/404/')
def error():
    return render_template('404error.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('login[username]')
        password = request.form.get('login[password]')
        user = User.query.filter(User.email == email).first()
        remember = request.form.get('remember')
        if user is not None and user.verify_password(password):
            login_user(user, remember=remember)
            return redirect(url_for('index'))
        else:
            # if the email has been registered, it cannot be registered again
            flash('Email or password is wrong. Please confirm before logging in!')
            return render_template('login.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form.get('register[email]')
        agree = request.form.get('agree')
        if agree is False:
            flash('Please agree the terms and conditions.')
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',email):
            #if re.match(r'[0-9a-zA-Z_]{0,19}@163.com',text):
            pass
        else:
            flash('The email format is wrong! Please try again!')
            return render_template('register.html')

        username = request.form.get('register[username]')
        password1 = request.form.get('register[password1]')
        password2 = request.form.get('register[password2]')
        # Mailbox verification, if it is registered, it cannot be registered again
        user = User.query.filter(User.email == email).first()
        if user:
            flash('The email has been registered! Please change one.')
            return render_template('register.html')
        else:
            # password1 must be equal to password2
            if password1 != password2:
                flash('Two passwords are not equal! Please check them before filling them in!')
                return render_template('register.html')
            else:
                user = User(email=email,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                # If the registration is successful, let the page jump to the login page
                return redirect(url_for('login'))


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/cart/')
@login_required
def cart():
    return render_template('shopping-cart.html')


@app.route('/product-detail/<product_id>', methods=['GET','POST'])
def productdetail(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    products = Product.query.all()
    return render_template('product-detail.html', product = product, products=products)


@app.route('/grid/')
def grid():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(per_page = 9, page = page, error_out = False)
    return render_template('grid.html', products=products)


@app.route('/wishlist/')
@login_required
def wishlist():
    return u'This is wishlist'


@app.route('/checkout/')
@login_required
def checkout():
    return u'This is chechout'


@app.route('/confirm-password/', methods=['GET', 'POST'])
@login_required
def confirm_password():
    if request.method == 'GET':
        return render_template('confirm-password.html')
    else:
        passwd = request.form.get('password')
        user = User.query.filter(User.email == current_user.email).first()
        if user.verify_password(passwd):
            return redirect(url_for('change_password'))
        else:
            flash('The password is wrong. Please try again!')
            return render_template('confirm-password.html')



@app.route('/change-password/', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template('change-password.html')
    else:
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('Two passwords are not equal! Please check them before filling them in!')
            return render_template('change-password.html')
        else:
            current_user.password = password1
            db.session.commit()
            # If the registration is successful, let the page jump to the login page
            return redirect(url_for('index'))



@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


if __name__ == '__main__':
    app.run()
