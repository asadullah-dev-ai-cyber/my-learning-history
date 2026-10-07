from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, Numeric, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    products: Mapped[List['Product']] = relationship('Product', back_populates='category')


class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(140), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    compare_at_price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(Integer, default=10)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    rating: Mapped[float] = mapped_column(Numeric(3, 2), default=5.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Foreign Key
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    # Relationships
    category: Mapped['Category'] = relationship('Category', back_populates='products')
    images: Mapped[List['ProductImage']] = relationship('ProductImage', back_populates='product', cascade='all, delete-orphan')


class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    # Foreign Key
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)

    # Relationship
    product: Mapped['Product'] = relationship('Product', back_populates='images')