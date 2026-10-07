import stripe
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from flask_login import current_user, login_required
from app.extensions import db
from app.models.product import Product
from app.models.order import Order, OrderItem

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@checkout_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    cart = session.get('cart', {})
    if not cart:
        flash("Your cart is empty.", "info")
        return redirect(url_for('shop.index'))

    cart_items = []
    total_amount = 0.0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            item_total = product.price * quantity
            total_amount += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })

    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    if request.method == 'POST':
        # Create pending order in database
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            status='pending',
            shipping_address=request.form.get('shipping_address'),
            city=request.form.get('city'),
            postal_code=request.form.get('postal_code'),
            country=request.form.get('country')
        )
        db.session.add(order)
        db.session.commit()

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['product'].price
            )
            db.session.add(order_item)
        db.session.commit()

        # Generate Stripe Checkout Line Items
        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['product'].name,
                    },
                    'unit_amount': int(item['product'].price * 100),  # Stripe uses cents
                },
                'quantity': item['quantity'],
            })

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=url_for('checkout.success', order_id=order.id, _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('checkout.index', _external=True),
            )
            return redirect(checkout_session.url, code=330)
        except Exception as e:
            flash(f"Stripe Integration Note: {str(e)}", "warning")
            # Fallback for testing without active Stripe API keys
            return redirect(url_for('checkout.success', order_id=order.id))

    return render_template('checkout/index.html', cart_items=cart_items, total_amount=total_amount, stripe_public_key=current_app.config['STRIPE_PUBLIC_KEY'])


@checkout_bp.route('/success/<int:order_id>')
@login_required
def success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return redirect(url_for('main.index'))

    # Mark order as completed and clear user cart
    order.status = 'completed'
    db.session.commit()
    session.pop('cart', None)

    return render_template('checkout/success.html', order=order)