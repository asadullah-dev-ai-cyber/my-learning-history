from flask import Blueprint, redirect, url_for, flash, request, jsonify, render_template
from flask_login import login_required, current_user
from app.extensions import db
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.social import Wishlist, Review
from app.forms.review import ReviewForm

social_bp = Blueprint('social', __name__)


@social_bp.route('/wishlist/toggle/<int:product_id>', methods=['POST'])
@login_required
def toggle_wishlist(product_id):
    product = Product.query.get_or_404(product_id)
    item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product.id).first()

    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Removed "{product.name}" from your wishlist.', 'info')
        added = False
    else:
        new_item = Wishlist(user_id=current_user.id, product_id=product.id)
        db.session.add(new_item)
        db.session.commit()
        flash(f'Added "{product.name}" to your wishlist.', 'success')
        added = True

    next_page = request.referrer or url_for('shop.catalog')
    return redirect(next_page)


@social_bp.route('/wishlist')
@login_required
def wishlist():
    user_wishlist = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('shop/wishlist.html', wishlist=user_wishlist)


@social_bp.route('/product/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()

    if form.validate_on_submit():
        # Check if user bought product (Verified Purchase)
        purchased = db.session.query(OrderItem).join(Order).filter(
            Order.user_id == current_user.id,
            OrderItem.product_id == product.id,
            Order.status == 'paid'
        ).first() is not None

        review = Review(
            product_id=product.id,
            user_id=current_user.id,
            rating=form.rating.data,
            title=form.title.data,
            comment=form.comment.data,
            is_verified=purchased
        )
        db.session.add(review)
        db.session.commit()
        flash('Thank you for your review!', 'success')
    else:
        flash('Failed to submit review. Please check your input.', 'danger')

    return redirect(url_for('shop.product_detail', slug=product.slug))