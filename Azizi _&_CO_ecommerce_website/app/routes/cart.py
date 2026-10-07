from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.models.product import Product

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


def get_cart_details():
    """Helper function to calculate cart totals and cast prices to float."""
    cart = session.get('cart', {})
    cart_items = []
    subtotal = 0.0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            # Cast Decimal price to float to prevent TypeError with subtotal
            price = float(product.price)
            item_total = price * int(quantity)
            subtotal += item_total

            cart_items.append({
                'product': product,
                'quantity': int(quantity),
                'price': price,
                'total_price': item_total
            })

    return cart_items, subtotal


@cart_bp.route('/')
def index():
    cart_items, subtotal = get_cart_details()
    shipping_cost = 0.0 if (subtotal > 150 or subtotal == 0) else 15.0
    grand_total = subtotal + shipping_cost

    return render_template(
        'cart/index.html',
        cart_items=cart_items,
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        grand_total=grand_total
    )


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))

    cart = session.get('cart', {})

    current_qty = cart.get(str(product_id), 0)
    new_qty = current_qty + quantity

    if new_qty > product.stock:
        flash(f"Only {product.stock} items available in stock.", "warning")
        cart[str(product_id)] = product.stock
    else:
        cart[str(product_id)] = new_qty
        flash(f"Added {product.name} to your cart.", "success")

    session['cart'] = cart
    session.modified = True

    return redirect(request.referrer or url_for('shop.index'))


@cart_bp.route('/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})

    if quantity > 0:
        cart[str(product_id)] = quantity
    else:
        cart.pop(str(product_id), None)

    session['cart'] = cart
    session.modified = True
    flash("Cart updated successfully.", "info")

    return redirect(url_for('cart.index'))


@cart_bp.route('/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)

    session['cart'] = cart
    session.modified = True
    flash("Item removed from cart.", "info")

    return redirect(url_for('cart.index'))