from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Category, Product, ProductImage

app = create_app('development')

def seed_database():
    with app.app_context():
        print("Clearing old data...")
        db.drop_all()
        db.create_all()

        print("Seeding admin user...")
        admin = User(
            full_name='Admin User',
            email='admin@azizi.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        print("Seeding categories...")
        tech = Category(name='Tech Accessories', slug='tech-accessories', description='Precision gadgets & luxury desk setups.')
        audio = Category(name='Audio', slug='audio', description='Studio-grade acoustic drivers & wireless sound.')
        wearables = Category(name='Wearables', slug='wearables', description='Next-generation smart tech and luxury timepieces.')
        lifestyle = Category(name='Lifestyle', slug='lifestyle', description='Curated carry gear and daily essentials.')
        apparel = Category(name='Apparel', slug='apparel', description='Minimalist streetwear and engineered activewear.')

        db.session.add_all([tech, audio, wearables, lifestyle, apparel])
        db.session.commit()

        print("Seeding 30+ luxury products...")
        products_data = [
            # Tech Accessories
            {
                'name': 'NOVA Vision Pro Stand', 'slug': 'nova-vision-pro-stand',
                'description': 'Precision CNC-machined matte obsidian aluminum stand with integrated magnetic fast charging.',
                'price': 149.00, 'compare_at': 189.00, 'stock': 25, 'featured': True, 'rating': 4.9, 'cat': tech,
                'img': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Apex Mechanical Keyboard V2', 'slug': 'apex-mechanical-keyboard-v2',
                'description': 'Custom gasket-mounted wireless mechanical keyboard with CNC chassis and hot-swappable switches.',
                'price': 240.00, 'compare_at': 290.00, 'stock': 15, 'featured': True, 'rating': 4.8, 'cat': tech,
                'img': 'https://images.unsplash.com/photo-1595225476474-87563907a212?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Obsidian Wireless Dock Duo', 'slug': 'obsidian-wireless-dock-duo',
                'description': 'Dual-device fast charging pad crafted from aerospace-grade aluminum and tempered glass.',
                'price': 110.00, 'compare_at': 140.00, 'stock': 30, 'featured': False, 'rating': 4.7, 'cat': tech,
                'img': 'https://images.unsplash.com/photo-1585338107529-13afc5f02586?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Titanium Precision Hub Pro', 'slug': 'titanium-precision-hub-pro',
                'description': '10-in-1 USB-C multiport hub featuring 4K HDMI 120Hz output and 100W power delivery.',
                'price': 95.00, 'compare_at': 120.00, 'stock': 40, 'featured': False, 'rating': 4.6, 'cat': tech,
                'img': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Luminary Desk Light Matrix', 'slug': 'luminary-desk-light-matrix',
                'description': 'Auto-dimming ambient LED monitor light bar with wireless desktop control dial.',
                'price': 130.00, 'compare_at': 160.00, 'stock': 18, 'featured': True, 'rating': 4.9, 'cat': tech,
                'img': 'https://images.unsplash.com/photo-1517732306149-e8f829eb588a?q=80&w=1000&auto=format&fit=crop'
            },

            # Audio
            {
                'name': 'CyberPulse ANC Headphones', 'slug': 'cyberpulse-anc-headphones',
                'description': 'Spatial audio studio-grade wireless headphones with custom 40mm beryllium drivers.',
                'price': 380.00, 'compare_at': 450.00, 'stock': 12, 'featured': True, 'rating': 5.0, 'cat': audio,
                'img': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Aura True Wireless Earbuds', 'slug': 'aura-true-wireless-earbuds',
                'description': 'Hybrid active noise cancellation earbuds with transparent acoustic chambers and lossless codec.',
                'price': 220.00, 'compare_at': 260.00, 'stock': 25, 'featured': True, 'rating': 4.8, 'cat': audio,
                'img': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Vortex Studio Monitor Speakers', 'slug': 'vortex-studio-monitor-speakers',
                'description': 'Powered bookshelf monitors with Kevlar woofers and Bluetooth 5.3 studio connectivity.',
                'price': 450.00, 'compare_at': 520.00, 'stock': 8, 'featured': True, 'rating': 5.0, 'cat': audio,
                'img': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'EchoStream USB-C Podcaster Mic', 'slug': 'echostream-usb-c-podcaster-mic',
                'description': 'Studio condenser microphone with internal pop filter, zero-latency monitoring, and RGB gain dial.',
                'price': 175.00, 'compare_at': 210.00, 'stock': 19, 'featured': False, 'rating': 4.7, 'cat': audio,
                'img': 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?q=80&w=1000&auto=format&fit=crop'
            },

            # Wearables
            {
                'name': 'Chronos Obsidian Smartwatch', 'slug': 'chronos-obsidian-smartwatch',
                'description': 'Aerospace titanium casing, sapphire crystal display, and advanced biometric health sensors.',
                'price': 499.00, 'compare_at': 599.00, 'stock': 14, 'featured': True, 'rating': 4.9, 'cat': wearables,
                'img': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Quantum Health Ring Gen-3', 'slug': 'quantum-health-ring-gen-3',
                'description': 'Discreet titanium sleep and recovery tracker with 7-day battery life and heart-rate analytics.',
                'price': 299.00, 'compare_at': 349.00, 'stock': 20, 'featured': True, 'rating': 4.8, 'cat': wearables,
                'img': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Horizon AR Smart Glasses', 'slug': 'horizon-ar-smart-glasses',
                'description': 'Lightweight augmented reality eyewear featuring micro-OLED heads-up displays and directional audio.',
                'price': 699.00, 'compare_at': 799.00, 'stock': 6, 'featured': True, 'rating': 4.7, 'cat': wearables,
                'img': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=1000&auto=format&fit=crop'
            },

            # Lifestyle
            {
                'name': 'Aegis Waterproof Tech Backpack', 'slug': 'aegis-waterproof-tech-backpack',
                'description': 'Weatherproof 25L daily carry pack with dedicated padded 16-inch laptop compartment.',
                'price': 195.00, 'compare_at': 240.00, 'stock': 18, 'featured': True, 'rating': 4.9, 'cat': lifestyle,
                'img': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Vanguard Insulated Steel Flask', 'slug': 'vanguard-insulated-steel-flask',
                'description': 'Double-wall vacuum insulated matte black bottle keeping beverages cold for 24 hours.',
                'price': 45.00, 'compare_at': 60.00, 'stock': 50, 'featured': False, 'rating': 4.7, 'cat': lifestyle,
                'img': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Zenith Ergonomic Leather Desk Mat', 'slug': 'zenith-ergonomic-leather-desk-mat',
                'description': 'Full-grain waterproof leather desk pad offering smooth mouse glide and scratch protection.',
                'price': 70.00, 'compare_at': 90.00, 'stock': 28, 'featured': False, 'rating': 4.8, 'cat': lifestyle,
                'img': 'https://images.unsplash.com/photo-1616440347437-b1c73416efc2?q=80&w=1000&auto=format&fit=crop'
            },

            # Apparel
            {
                'name': 'Hyperweave Technical Hoodie', 'slug': 'hyperweave-technical-hoodie',
                'description': 'Engineered moisture-wicking fleece hoodie with hidden zippered security pockets.',
                'price': 135.00, 'compare_at': 170.00, 'stock': 20, 'featured': True, 'rating': 4.8, 'cat': apparel,
                'img': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Apex All-Weather Softshell Jacket', 'slug': 'apex-all-weather-softshell-jacket',
                'description': 'Windproof and water-repellent urban shell jacket with bonded internal thermal lining.',
                'price': 210.00, 'compare_at': 260.00, 'stock': 15, 'featured': True, 'rating': 4.9, 'cat': apparel,
                'img': 'https://images.unsplash.com/photo-1544441893-675973e31985?q=80&w=1000&auto=format&fit=crop'
            },
            {
                'name': 'Eclipse Heavyweight Cotton Tee', 'slug': 'eclipse-heavyweight-cotton-tee',
                'description': 'Relaxed-fit luxury organic cotton t-shirt with pigment-dyed finish and durable collar ribbing.',
                'price': 55.00, 'compare_at': 70.00, 'stock': 40, 'featured': False, 'rating': 4.6, 'cat': apparel,
                'img': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=1000&auto=format&fit=crop'
            }
        ]

        for p_data in products_data:
            product = Product(
                name=p_data["name"],
                slug=p_data["slug"],
                description=p_data["description"],
                price=p_data["price"],
                compare_at_price=p_data["compare_at"],
                stock=p_data["stock"],
                rating=p_data["rating"],
                is_featured=p_data["featured"],
                is_active=True,
                category_id=p_data["cat"].id
            )
            db.session.add(product)
            db.session.commit()

            image = ProductImage(product_id=product.id, image_url=p_data["img"], is_primary=True)
            db.session.add(image)
            db.session.commit()

        print("Database re-seeded successfully with full collection!")

if __name__ == '__main__':
    seed_database()