from flask import Flask, render_template, request, url_for, redirect, g, flash, jsonify
import config
from exts import db
from models import User, Product, Cart_product, Anonymous, Profile, Address, Review
import re
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.anonymous_user = Anonymous
login_manager.init_app(app)


# 默认日志等级的设置
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器，指明日志保存路径,每个日志的大小，保存日志的上限
file_log_handler = RotatingFileHandler('all.log', maxBytes=1024 * 1024, backupCount=10)
# 设置日志的格式                   发生时间    日志等级     日志信息文件名      函数名          行数        日志信息
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
# 将日志记录器指定日志的格式
file_log_handler.setFormatter(formatter)
# 日志等级的设置
# file_log_handler.setLevel(logging.WARNING)
# 为全局的日志工具对象添加日志记录器
logging.getLogger().addHandler(file_log_handler)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
def index():
    products = Product.query.all()
    ip = request.remote_addr # get the ip of the visit
    app.logger.debug("The user ip is " + ip)
    version = str(request.user_agent)  # get the hardware and browser version info of the visit
    app.logger.debug("The hardware version and browser info is " + version)
    return render_template('index.html', products = products)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('login[username]')
        password = request.form.get('login[password]')
        user = User.query.filter(User.email == email).first()
        remember = request.form.get('remember')
        # Keep logging in until the user logs out if remember is True
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
    # logout will delete the user session
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
    # print(Cart_product.query.filter(Cart_product.product_id == product_id, Cart_product.user_id == current_user.id))
    if cart_product:
        cart_product.number += num
        db.session.commit()
        info = "In table Cart_product of user id " + str(current_user.id) + ", the number of product of id " + str(cart_product) + " number add " + str(cart_product.number)
        app.logger.info(info)
    else:
        cart_product = Cart_product(user_id=current_user.id, product_id=product_id)
        cart_product.number = num
        db.session.add(cart_product)
        db.session.commit()
        info = "In table Cart_product of user id " + str(current_user.id) + ", the number of product of id " + str(cart_product) + " is added. Number is " + str(cart_product.number)
        app.logger.info(info)
    return jsonify({'result': 'success'})
    # return redirect(url_for('grid'))


@app.route('/delete_cart_product/', methods=['POST'])
@login_required
def delete_cart_product():
    product_id = request.form.get('product_id')
    # print(product_id)
    product = Cart_product.query.filter(Cart_product.product_id == product_id, Cart_product.user_id == current_user.id).first()
    db.session.delete(product)
    info = "In table Cart_product of user id " + str(current_user.id) + ", the number of product of id " + str(product_id) + " is deleted!"
    app.logger.info(info)
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
    info = "In table Cart_product of user id " + str(current_user.id) + ", the number of product of id " + str(product_id) + " is changed to " + str(number)
    app.logger.info(info)
    total_price = 0
    for cart_product in cart_products:
        total_price += cart_product.number * cart_product.product.price
    return jsonify({'result': 'success', 'total_price': total_price})


@app.route('/product-detail/<product_id>', methods=['GET', 'POST'])
def productdetail(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    products = Product.query.all()
    product_more = products[0:5]
    reviews = Review.query.filter(Review.product_id == product_id)
    review_num = Review.query.filter(Review.product_id == product_id).count()
    profile = Profile.query.filter(Profile.profile_id == current_user.id).first()
    return render_template('product-detail.html', product = product, products=products,product_more=product_more, reviews=reviews, review_num=review_num, profile=profile)


@app.route('/grid/')
def grid():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(per_page=9, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/sort_less100/')
def sort_less100():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.price < 100).paginate(per_page=20, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/sort_above100/')
def sort_above100():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.price >= 100).paginate(per_page=20, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/sort_green/')
def sort_green():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.color == 'green').paginate(per_page=20, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/sort_red/')
def sort_red():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.color == 'red').paginate(per_page=20, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/sort_yellow/')
def sort_yellow():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.color == 'yellow').paginate(per_page=20, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/sort_purple/')
def sort_purple():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.color == 'purple').paginate(per_page=20, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/sort_small/')
def sort_small():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.size == 'Small').paginate(per_page=20, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/sort_medium/')
def sort_medium():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.size == 'Middle').paginate(per_page=20, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/sort_large/')
def sort_large():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.size == 'Large').paginate(per_page=20, page=page, error_out=False)
    return render_template('grid.html', products=products)


@app.route('/sort_keyword/', methods=['POST'])
def sort_keyword():
    keyword = request.form.get('keyword')
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.name.contains(keyword)).paginate(per_page=20, page=page, error_out=False)
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


@app.route('/editProfile', methods = ['POST'])
def editProfile():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        first_Name = request.form.get('firstname')
        last_Name = request.form.get('lastname')
        message = request.form.get('message')
        company = request.form.get('company')
        telephone = request.form.get('telephone')
        fax = request.form.get('fax')
        photo_path = "upload/" + f.filename
        profile = Profile.query.filter(Profile.profile_id == current_user.id).first()
        if profile:
            profile.first_Name = first_Name
            profile.last_Name = last_Name
            profile.message = message
            profile.company = company
            profile.photo_path = photo_path
            profile.telephone = telephone
            profile.fax = fax
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            profile = Profile(profile_id=current_user.id, first_Name=first_Name, last_Name=last_Name, message=message, company=company, photo_path=photo_path, telephone=telephone, fax=fax)
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for('dashboard'))


@app.route('/add_address/', methods=['GET', 'POST'])
def add_address():
    if request.method == 'GET':
        return render_template('checkout-billing-info.html')
    else:
        street = request.form.get('street')
        city = request.form.get('city')
        region = request.form.get('region')
        postcode = request.form.get('postcode')
        country = request.form.get('country')
        radio = request.form.get('inlineRadioOptions')
        if radio == 'default':
            isdefault = True
        else:
            isdefault = False
        address = Address(user_id=current_user.id, street=street, city=city, province=region, country=country, postcode=postcode, default_address=isdefault)
        db.session.add(address)
        db.session.commit()
        return redirect(url_for('dashboard'))


@app.route('/delete_address/', methods=['POST'])
def delete_address():
    address_id = request.form.get('address_id')
    address = Address.query.filter(Address.address_id == address_id).first()
    db.session.delete(address)
    db.session.commit()
    return jsonify({'result': 'success'})


@app.route('/add_review/', methods=['POST'])
def add_review():
    product_id = request.form.get('product_id')
    rating = request.form.get('rating')
    content = request.form.get('content')
    review = Review(user_id=current_user.id, rating=rating, content=content, product_id=product_id)
    db.session.add(review)
    db.session.commit()
    return jsonify({'result': 'success'})


@app.route('/orderDetails/', methods=['GET', 'POST'])



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
