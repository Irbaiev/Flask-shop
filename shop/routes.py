import os
from sqlalchemy import false, true
from shop import app, login_manager
from flask import render_template, request, redirect, url_for, flash
from shop.models import Product, db, User, Buy
from PIL import Image
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user
from flask import session
from shop.form import RegistrationForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        file_name = request.files.get('image')
        filename = secure_filename(file_name.filename)
        file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        f = request.form
        p = Product(title=f.get('title'), price=f.get('price'), category=f.get('category'), availibility=f.get('availibility'), description=f.get('description'), image=file_name.filename)
        db.session.add(p)
        db.session.commit()
    return render_template('add_product.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(email = request.form.get('email')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout', methods = ['GET', 'POST'])
def log_out():
    logout_user()
    return redirect(url_for('index'))


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    return render_template('product_detail.html', product=product)
    

@app.route('/shops/<int:product_id>/del/')
def product_delete(product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return redirect ('/shop')


@app.route('/register', methods =['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration completed successfully!', 'success')
        return redirect(url_for('login'))
    return render_template ('registration.html', form=form)


@app.route('/products/<int:product_id>/buy', methods=['GET', 'POST'])
def buy(product_id):
    product = Product.query.get(product_id)
    if request.method == "POST":
        f = request.form
        b = Buy(name=f.get('name'), adress=f.get('adress'), email=f.get(
            'email'), product=product)
        db.session.add(b)
        db.session.commit()
        return redirect ('/buys')
    return render_template('buy.html')


@app.route('/buys')
def buys():
    buys = Buy.query.all()
    return render_template('buys.html', buys=buys)


@app.route('/shops/<int:buy_id>/del/')
def buy_delete(buy_id):
        buy = Buy.query.get_or_404(buy_id)
        db.session.delete(buy)
        db.session.commit()
        return redirect ('/shop')