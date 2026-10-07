import stripe
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required, current_user
from app.models.order import Order
from app.extensions import db

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')


@payment_bp.route('/checkout-session/<int:order_id>', methods=['POST'])
@login_required
def create_checkout_session(order_id):
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        flash('Unauthorized access to order.', 'danger')
        return redirect(url_for('shop.catalog'))

    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    line_items = []
    for item in order.items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.price * 100),  # Amount in cents
            },
            'quantity': item.quantity,
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            client_reference_id=str(order.id),
            success_url=url_for('payment.success', order_id=order.id, _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('payment.cancel', order_id=order.id, _external=True),
            customer_email=current_user.email,
        )
        return redirect(checkout_session.url, code=330)
    except Exception as e:
        flash(f'Payment initialization error: {str(e)}', 'danger')
        return redirect(url_for('orders.order_detail', order_id=order.id))


@payment_bp.route('/success/<int:order_id>')
@login_required
def success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('shop.catalog'))

    session_id = request.args.get('session_id')
    if session_id:
        order.status = 'paid'
        db.session.commit()

    return render_template('payment/success.html', order=order)


@payment_bp.route('/cancel/<int:order_id>')
@login_required
def cancel(order_id):
    order = Order.query.get_or_404(order_id)
    flash('Payment process was cancelled.', 'warning')
    return redirect(url_for('orders.order_detail', order_id=order.id))