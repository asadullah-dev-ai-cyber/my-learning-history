from flask import Blueprint, render_template
from app.models.product import Product, Category

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    products = Product.query.filter_by(is_active=True).all()
    categories = Category.query.all()
    featured_products = Product.query.filter_by(is_featured=True, is_active=True).all()

    return render_template(
        'main/index.html',
        products=products,
        categories=categories,
        featured=featured_products
    )