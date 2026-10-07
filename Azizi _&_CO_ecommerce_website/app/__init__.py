from flask import Flask, session
from config import config
from app.extensions import db, migrate, login_manager
from flask_wtf.csrf import CSRFProtect
from app.extensions import db, migrate, login_manager, cache

csrf = CSRFProtect()
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)

    # Configure Login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Ensure all models are loaded before tables are queried or created
    from app.models.user import User
    from app.models.product import Category, Product, ProductImage
    from app.models.cart import Cart, CartItem
    from app.models.order import Order, OrderItem

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Automatically create missing tables and seed basic data
    with app.app_context():
        db.create_all()

        # Seed default admin user if not existing
        admin_user = User.query.filter_by(email='admin@azizi.com').first()
        if not admin_user:
            admin_user = User(
                full_name='Admin User',
                email='admin@azizi.com',
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()

        if not Category.query.first():
            tech = Category(name='Tech Accessories', slug='tech-accessories', description='Premium tech gadgets & luxury desk setups.')
            apparel = Category(name='Apparel', slug='apparel', description='Minimalist streetwear and engineered activewear.')
            lifestyle = Category(name='Lifestyle', slug='lifestyle', description='Curated carry gear and daily essentials.')

            db.session.add_all([tech, apparel, lifestyle])
            db.session.commit()

            p1 = Product(
                name='NOVA Vision Pro Stand',
                slug='nova-vision-pro-stand',
                description='Precision CNC-machined matte obsidian aluminum stand with integrated magnetic fast charging.',
                price=149.00,
                compare_at_price=189.00,
                stock=25,
                is_featured=True,
                rating=4.9,
                category_id=tech.id
            )

            p2 = Product(
                name='CyberPulse ANC Headphones',
                slug='cyberpulse-anc-headphones',
                description='Spatial audio studio-grade wireless headphones with custom 40mm beryllium drivers.',
                price=380.00,
                compare_at_price=450.00,
                stock=12,
                is_featured=True,
                rating=5.0,
                category_id=tech.id
            )

            db.session.add_all([p1, p2])
            db.session.commit()

            img1 = ProductImage(product_id=p1.id, image_url='https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?q=80&w=1000&auto=format&fit=crop', is_primary=True)
            img2 = ProductImage(product_id=p2.id, image_url='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=1000&auto=format&fit=crop', is_primary=True)

            db.session.add_all([img1, img2])
            db.session.commit()

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.shop import shop_bp
    from app.routes.cart import cart_bp
    from app.routes.auth import auth_bp
    from app.routes.checkout import checkout_bp
    from app.routes.admin import admin_bp
    from app.routes.webhook import webhook_bp
    from app.routes.payment import payment_bp
    from app.routes.social import social_bp


    app.register_blueprint(social_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(admin_bp)

    # Context Processor for Cart Badge Counter
    @app.context_processor
    def inject_cart_count():
        cart = session.get('cart', {})
        total_items = sum(cart.values())
        return dict(cart_count=total_items)

    csrf.init_app(app)
    return app