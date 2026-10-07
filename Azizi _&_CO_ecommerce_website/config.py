import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'azizi-co-super-secret-key-2026')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    # Stripe Configuration
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_sample_key')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_sample_key')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

    # Security Headers & Cookie Hardening
    SESSION_COOKIE_SECURE = False  # If True, Only send cookies over HTTPS (set False during local HTTP development)
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie (mitigates XSS)
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protects against CSRF on cross-site requests
    PERMANENT_SESSION_LIFETIME = 1800  # Session timeout in seconds (30 mins)



class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL',
        f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


# Mapping dictionary imported by app factory
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}