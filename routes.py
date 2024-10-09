from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify

from models import User, Product, Cart, Discount,  Category,Favorite,Contact,Review
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  
from app import app 
import re
from flask_login import login_required
from app import app,mail
from flask_mail import Mail, Message
from models import OTP  
from datetime import datetime, timedelta
import random

import requests



@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)  
    return render_template('product_detail.html', product=product)
@app.route('/home')
@app.route('/')
@app.route('/category/<string:category>')
def home(category=None):
    categories = Category.query.all() 
    if category:
        category_obj = Category.query.filter_by(title=category).first_or_404()
        products = Product.query.filter_by(category_id=category_obj.id).all()
    else:
        products = Product.query.all()
    
    categories = Category.query.all()
    return render_template('shop.html', products=products, categories=categories, current_category=category)
@app.route('/discounted-products')
def discounted_products():
    discounted_products = Product.query.filter(
        Product.discount_price.isnot(None),
        Product.new_price > Product.discount_price
    ).all()
    return render_template('discounted_products.html', products=discounted_products)

@app.route('/detail', methods=['GET', 'POST'])
def detail():
    return render_template('detail.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if not user.is_verified:
                flash('Please verify your email before logging in.', 'warning')
                return redirect(url_for('login'))

            session['user_id'] = user.id
            session['user_name'] = user.name
            session['is_admin'] = user.is_admin 
            
            return redirect(url_for('home'))
        else:
            flash('Invalid login credentials', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))
def is_password_complex(password):
    return (len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

import random
import string
from flask import request, flash, redirect, url_for, render_template
from flask_mail import Message
from extensions import db, mail
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not is_password_complex(password):
            flash('Password must be at least 8 characters long and include a capital letter, a lowercase letter, a number, and a special character.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email address already exists. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        otp = ''.join(random.choices(string.digits, k=6))  
        hashed_password = generate_password_hash(password)  

        new_user = User(name=name, email=email, password=hashed_password, otp=otp)

        msg = Message("Your OTP Code", recipients=[email])
        msg.body = f"Your OTP code is: {otp}"
        mail.send(msg)

        db.session.add(new_user)
        db.session.commit()

        flash('An OTP has been sent to your email. Please verify it to complete registration.', 'info')
        return redirect(url_for('verify_otp', email=email))

    return render_template('register.html')

@app.route('/category/<category_name>')
def category_products(category_name):
    if category_name == 'all':
        products = Product.query.all()  
    else:
        category = Category.query.filter_by(title=category_name).first()
        products = Product.query.filter_by(category_id=category.id).all()
    
    return render_template('shop.html', products=products, current_category=category_name)
    
    return render_template('category.html', category=category, products=products)
@app.route('/profile/', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your profile', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if user:
        return render_template('profile.html', user=user)
    return "User not found", 404


@app.route('/product/<int:product_id>')
def product_details(product_id):
    return render_template('product_details.html')



@app.route('/products')
def product_list():
    return render_template('products.html')

from flask import send_file, abort
from io import BytesIO

@app.route('/image/<int:product_id>')
def serve_image(product_id):
    product = Product.query.get_or_404(product_id)
    if not product.image:
        abort(404)
    return send_file(BytesIO(product.image), mimetype='image/jpeg')



@app.route('/favorites')
def favorites_list():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your favorites', 'warning')
        return redirect(url_for('login'))

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorite_products = [favorite.product for favorite in favorites]
    return render_template('favorites.html', favorites=favorite_products)




@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        new_contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')
@app.route('/basket')
def basket():
    return render_template('basket.html')



 

@app.route('/shop', methods=['GET'])
def shop():
    categories = Category.query.all()

    selected_category = request.args.get('category')  
    if selected_category:
        products = Product.query.filter_by(category_id=selected_category).all() 
    else:
        products = Product.query.all()  

    return render_template('shop.html', categories=categories, products=products, current_category=selected_category)


@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    product_id = request.form.get('product_id')
    user_id = session.get('user_id')

    if user_id and product_id:
        existing_favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()

        if existing_favorite:
            flash('This product is already in your favorites!', 'warning')
        else:
            favorite = Favorite(product_id=product_id, user_id=user_id)
            db.session.add(favorite)
            db.session.commit()
            flash('Product added to favorites!', 'success')

        return redirect(url_for('product_detail', product_id=product_id))

    return render_template('login.html')

@app.route('/remove_from_favorites', methods=['POST'])
def remove_from_favorites():
    user_id = session.get('user_id')
    product_id = request.form.get('product_id')

    if user_id and product_id:
        favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            flash('Product removed from favorites!', 'success')
        else:
            flash('Product not found in favorites.', 'warning')
    else:
        flash('User not logged in or invalid product ID.', 'danger')

    return redirect(url_for('favorites_list'))

@app.route('/search', methods=['GET','POST'])
def search():
    query = request.args.get('query', '').strip()
    
    if query:
        products = Product.query.filter(
            db.or_(
                Product.name.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%')
            )
        ).all()
    else:
        products = []

    return render_template('search_results.html', products=products, query=query)

@app.route('/add_review', methods=['POST'])
def add_review():
  
    user_name = session.get('user_name')
    if not user_name:
        flash('You must be logged in to leave a review.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        content = request.form.get('content')

    
        if not content:
            flash('Review content is required!', 'danger')
            return redirect(url_for('product_detail', product_id=product_id)) 

        user_id = session.get('user_id')  

       
        new_review = Review(product_id=product_id, user_id=user_id, content=content)
        db.session.add(new_review)
        db.session.commit()
        
        flash('Your review has been added!', 'success')
        return redirect(url_for('product_detail', product_id=product_id))


@app.route('/verify_otp/<email>', methods=['GET', 'POST'])
def verify_otp(email):
    user = User.query.filter_by(email=email).first()
    if request.method == 'POST':
        otp = request.form['otp']
        
        if user and user.otp == otp:
            user.is_verified = True
            db.session.commit()
            flash('Your email has been verified!', 'success')
            return redirect(url_for('login'))  
        else:
            flash('Invalid OTP. Please try again.', 'danger')
    
    return render_template('verify_otp.html', email=email)




@app.context_processor
def inject_categories():
    categories = Category.query.all() 
    return dict(categories=categories)
@app.context_processor
def inject_cart_and_favorites_count():
    user_id = session.get('user_id')  
    if user_id:
        favorites_count = Favorite.query.filter_by(user_id=user_id).count() 
        cart_count = Cart.query.filter_by(user_id=user_id).count()  
    else:
        favorites_count = 0
        cart_count = 0

    return dict(favorites_count=favorites_count, cart_count=cart_count)

if __name__ == '__main__':
    app.run(debug=True)