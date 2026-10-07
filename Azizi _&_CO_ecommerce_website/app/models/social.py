from datetime import datetime
from app.extensions import db


class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    product = db.relationship('Product', backref=db.backref('wishlist_items', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('wishlist_items', cascade='all, delete-orphan'))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_wishlist'),
    )


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    title = db.Column(db.String(120), nullable=True)
    comment = db.Column(db.Text, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    product = db.relationship('Product', backref=db.backref('reviews', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('reviews', cascade='all, delete-orphan'))