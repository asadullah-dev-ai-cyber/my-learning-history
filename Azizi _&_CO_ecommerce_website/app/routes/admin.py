from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models.product import Product, Category, ProductImage
from app.models.order import Order
from app.models.user import User
from app.forms.admin import ProductForm
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0.0
    total_orders = Order.query.count()
    total_products = Product.query.count()
    total_users = User.query.count()

    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_products=total_products,
        total_users=total_users,
        recent_orders=recent_orders
    )


@admin_bp.route('/products')
@login_required
@admin_required
def products():
    all_products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=all_products)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            slug=form.slug.data.lower().replace(' ', '-'),
            description=form.description.data,
            price=float(form.price.data),
            compare_at_price=float(form.compare_at_price.data) if form.compare_at_price.data else None,
            stock=form.stock.data,
            rating=float(form.rating.data or 5.0),
            category_id=form.category_id.data,
            is_featured=form.is_featured.data,
            is_active=form.is_active.data
        )
        db.session.add(product)
        db.session.flush()

        img = ProductImage(product_id=product.id, image_url=form.image_url.data, is_primary=True)
        db.session.add(img)

        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, title="Add New Product")


@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    primary_img = ProductImage.query.filter_by(product_id=product.id, is_primary=True).first()

    if request.method == 'GET' and primary_img:
        form.image_url.data = primary_img.image_url

    if form.validate_on_submit():
        product.name = form.name.data
        product.slug = form.slug.data.lower().replace(' ', '-')
        product.description = form.description.data
        product.price = float(form.price.data)
        product.compare_at_price = float(form.compare_at_price.data) if form.compare_at_price.data else None
        product.stock = form.stock.data
        product.rating = float(form.rating.data or 5.0)
        product.category_id = form.category_id.data
        product.is_featured = form.is_featured.data
        product.is_active = form.is_active.data

        if primary_img:
            primary_img.image_url = form.image_url.data
        else:
            new_img = ProductImage(product_id=product.id, image_url=form.image_url.data, is_primary=True)
            db.session.add(new_img)

        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, title="Edit Product")


@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully.", "info")
    return redirect(url_for('admin.products'))