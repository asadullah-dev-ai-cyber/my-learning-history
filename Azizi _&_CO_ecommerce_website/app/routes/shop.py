from flask import Blueprint, render_template, request
from app.models.product import Product, Category
from app.extensions import cache

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')

@shop_bp.route('/')
# MUST include query_string=True so the cache respects ?page=2 and ?category=lifestyle
@cache.cached(timeout=60, query_string=True)
def index():
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category')
    search_query = request.args.get('q', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'newest')

    query = Product.query.filter_by(is_active=True)

    # Search filter
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%') | Product.description.ilike(f'%{search_query}%'))

    # Category filter
    selected_category = None
    if category_slug:
        selected_category = Category.query.filter_by(slug=category_slug).first()
        if selected_category:
            # Using join ensures we filter purely by the relationship
            query = query.join(Category).filter(Category.slug == category_slug)

    # Price range filter
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Sorting
    if sort_by == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    # Pagination (6 items per page)
    pagination = query.paginate(page=page, per_page=6, error_out=False)
    products = pagination.items
    categories = Category.query.all()

    return render_template(
        'shop/index.html',
        products=products,
        pagination=pagination,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by
    )

@shop_bp.route('/product/<slug>')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()

    return render_template('shop/detail.html', product=product, related_products=related_products)