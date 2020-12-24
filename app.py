from flask import Flask, render_template, request, url_for, redirect, session, g
import config
from exts import db
from models import User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


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
        user = User.query.filter(User.email == email, User.password == password).first()
        canPass = False
        if user:
            session['user_id'] = user.id
            # if do not want to log in in 30 days
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', canPass = canPass)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form.get('register[email]')
        username = request.form.get('register[username]')
        password1 = request.form.get('register[password1]')
        password2 = request.form.get('register[password2]')
        # Mailbox verification, if it is registered, it cannot be registered again
        user = User.query.filter(User.email == email).first()
        if user:
            hasRegistered = False
            return render_template('register.html', hasRegistered = hasRegistered)
        else:
            # password1 must be equal to password2
            if password1 != password2:
                canPass = False
                return render_template('register.html', canPass = canPass)
            else:
                user = User(email=email,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                # If the registration is successful, let the page jump to the login page
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/cart/')
def cart():
    return render_template('shopping-cart.html')


@app.route('/product-detail/')
def productdetail():
    return render_template('product-detail.html')


@app.route('/grid/')
def grid():
    return render_template('grid.html')


@app.route('/wishlist/')
def wishlist():
    return u'This is wishlist'


@app.route('/checkout/')
def checkout():
    return u'This is chechout'



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
