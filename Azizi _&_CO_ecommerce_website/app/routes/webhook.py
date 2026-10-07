import stripe
from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.models.order import Order

webhook_bp = Blueprint('webhook', __name__, url_prefix='/webhook')


@webhook_bp.route('/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')

    try:
        if endpoint_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        else:
            event = request.get_json()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Handle payment success event
    if event.get('type') == 'checkout.session.completed':
        session_obj = event['data']['object']
        order_id = session_obj.get('client_reference_id')

        if order_id:
            order = Order.query.get(int(order_id))
            if order:
                order.status = 'paid'
                db.session.commit()

    return jsonify({'status': 'success'}), 200