from flask import Flask, render_template, request, url_for, redirect, session, g, flash, jsonify
import config
from exts import db
from models import User, Product, Cart_product, Anonymous, Profile, Address
import re
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.anonymous_user = Anonymous
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products = products)


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
    profile = Profile.query.filter(Profile.profile_id == current_user.id).first()
    return render_template('dashboard.html', current_user = current_user, profile=profile)


@app.route('/cart/')
@login_required
def cart():
    return render_template('shopping-cart.html')


@app.route('/addcart/', methods=['POST'])
@login_required
def add_cart():
    product_id = request.form.get('product_id')
    product_num = request.form.get('num')
    if product_num:
        num = int(product_num)
    else:
        num = 1
    cart_product = Cart_product.query.filter(Cart_product.product_id == product_id, Cart_product.user_id == current_user.id).first()
    if cart_product:
        cart_product.number += num
        db.session.commit()
    else:
        cart_product = Cart_product(user_id=current_user.id, product_id=product_id)
        cart_product.number = num
        db.session.add(cart_product)
        db.session.commit()
    return jsonify({'result': 'success'})
    # return redirect(url_for('grid'))


@app.route('/delete_cart_product/', methods=['POST'])
@login_required
def delete_cart_product():
    product_id = request.form.get('product_id')
    # print(product_id)
    product = Cart_product.query.filter(Cart_product.product_id == product_id, Cart_product.user_id == current_user.id).first()
    db.session.delete(product)
    db.session.commit()
    return jsonify({'result': 'success'})


@app.route('/change_product_num/', methods=['POST'])
@login_required
def change_product_num():
    product_id = request.form.get('product_id')
    number = request.form.get('num')
    cart_product = Cart_product.query.filter(Cart_product.product_id == product_id, Cart_product.user_id == current_user.id).first()
    cart_product.number = number
    db.session.commit()
    cart_products = Cart_product.query.filter(Cart_product.user_id == current_user.id).all()
    total_price = 0
    for cart_product in cart_products:
        total_price += cart_product.number * cart_product.product.price
    return jsonify({'result': 'success', 'total_price': total_price})


@app.route('/product-detail/<product_id>', methods=['GET', 'POST'])
def productdetail(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    products = Product.query.all()
    product_more = products[0:5]
    return render_template('product-detail.html', product = product, products=products,product_more=product_more)


@app.route('/grid/')
def grid():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(per_page=9, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/clear-cart/', methods=['POST'])
@login_required
def clear_cart():
    cart_products = Cart_product.query.filter(Cart_product.user_id == current_user.id).all()
    for product in cart_products:
        db.session.delete(product)
    db.session.commit()
    # return render_template('shopping-cart.html')
    return redirect(url_for('cart'))



@app.route('/wishlist/')
@login_required
def wishlist():
    return u'This is wishlist'


@app.route('/profile/')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/editProfile', methods = ['GET', 'POST'])
def editProfile():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        first_Name = request.form.get('firstname')
        last_Name = request.form.get('lastname')
        message = request.form.get('lastname')
        company = request.form.get('company')
        photo_path = "/upload/" + f.filename
        profile = Profile.query.filter(Profile.profile_id == current_user.id).first()
        if profile:
            profile.first_Name = first_Name
            profile.last_Name = last_Name
            profile.message = message
            profile.company = company
            profile.photo_path = photo_path
            db.session.commit()
        else:
            profile = Profile(profile_id=current_user.id, first_Name=first_Name, last_Name=last_Name, message=message, company=company, photo_path=photo_path)
            db.session.add(profile)
            db.session.commit()
    return render_template('dashboard.html', profile=profile)


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
    cart_products = Cart_product.query.filter(Cart_product.user_id == current_user.id).all()
    g.cart_products_num = Cart_product.query.filter(Cart_product.user_id == current_user.id).count()
    g.cart_products = cart_products
    total_price = 0
    for cart_product in cart_products:
        total_price += cart_product.number * cart_product.product.price
    g.total_price = total_price


# @app.context_processor
# def my_context_processor():
#     if hasattr(g, 'user'):
#         return {'user': g.user}
#     return {}


if __name__ == '__main__':
    app.run()
