from app import app
from models import User, Product, Category, Contact, Review  
from extensions import db
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/img' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin', methods=['GET', 'POST'])
def admin_profile():
    if not session.get('is_admin'):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

   
    users = User.query.all()
    products = Product.query.all()
    categories = Category.query.all()
    contacts = Contact.query.all()
    reviews = Review.query.all()

    if request.method == 'POST':
        action = request.form.get('action')
        entity_type = request.form.get('entity_type')
        entity_id = request.form.get('entity_id')

        
        if entity_type == 'user':
            if action == 'delete' and entity_id:
                user_to_delete = User.query.get(entity_id)
                if user_to_delete:
                    db.session.delete(user_to_delete)
                    db.session.commit()
                    flash('User deleted successfully.', 'success')
                else:
                    flash('User not found.', 'danger')

            elif action == 'edit' and entity_id:
                user_to_edit = User.query.get(entity_id)
                if user_to_edit:
                    user_to_edit.name = request.form.get('name', user_to_edit.name)
                    user_to_edit.email = request.form.get('email', user_to_edit.email)
                    user_to_edit.is_admin = request.form.get('is_admin') == 'on'
                    db.session.commit()
                    flash('User updated successfully.', 'success')
                else:
                    flash('User not found.', 'danger')

            elif action == 'add':
                new_user = User(
                    name=request.form.get('name'),
                    email=request.form.get('email'),
                    password=request.form.get('password'), 
                    is_admin=request.form.get('is_admin') == 'on',
                    otp='123456' 
                )
                db.session.add(new_user)
                db.session.commit()
                flash('User added successfully.', 'success')

        
        elif entity_type == 'product':
            if action == 'delete' and entity_id:
                product_to_delete = Product.query.get(entity_id)
                if product_to_delete:
                    db.session.delete(product_to_delete)
                    db.session.commit()
                    flash('Product deleted successfully.', 'success')
                else:
                    flash('Product not found.', 'danger')

            elif action == 'edit' and entity_id:
                product_to_edit = Product.query.get(entity_id)
                if product_to_edit:
                    product_to_edit.name = request.form.get('name', product_to_edit.name)
                    product_to_edit.description = request.form.get('description', product_to_edit.description)
                    product_to_edit.new_price = request.form.get('new_price', product_to_edit.new_price)
                    product_to_edit.discount_price = request.form.get('discount_price', product_to_edit.discount_price)
                    product_to_edit.category_id = request.form.get('category_id', product_to_edit.category_id)

                    
                    if 'image' in request.files:
                        file = request.files['image']
                        if file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            product_to_edit.image = filename 

                    db.session.commit()
                    flash('Product updated successfully.', 'success')
                else:
                    flash('Product not found.', 'danger')

            elif action == 'add':
                new_product = Product(
                    name=request.form.get('name'),
                    description=request.form.get('description'),
                    new_price=request.form.get('new_price'),
                    discount_price=request.form.get('discount_price'),
                    category_id=request.form.get('category_id')
                )

                if 'image' in request.files:
                    file = request.files['image']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        new_product.image = filename 

                db.session.add(new_product)
                db.session.commit()
                flash('Product added successfully.', 'success')

        elif entity_type == 'contact':
            if action == 'delete' and entity_id:
                contact_to_delete = Contact.query.get(entity_id)
                if contact_to_delete:
                    db.session.delete(contact_to_delete)
                    db.session.commit()
                    flash('Contact message deleted successfully.', 'success')
                else:
                    flash('Contact message not found.', 'danger')

        elif entity_type == 'review':
            if action == 'delete' and entity_id:
                review_to_delete = Review.query.get(entity_id)
                if review_to_delete:
                    db.session.delete(review_to_delete)
                    db.session.commit()
                    flash('Review deleted successfully.', 'success')
                else:
                    flash('Review not found.', 'danger')

    return render_template('admin.html', users=users, products=products, categories=categories, contacts=contacts, reviews=reviews)
