from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=120)])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price ($)', validators=[DataRequired(), NumberRange(min=0)])
    compare_at_price = DecimalField('Compare at Price ($)', validators=[Optional(), NumberRange(min=0)])
    stock = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    rating = DecimalField('Rating (0-5)', default=5.0, validators=[Optional(), NumberRange(min=0, max=5)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    is_featured = BooleanField('Featured Product')
    is_active = BooleanField('Active in Store', default=True)
    image_url = StringField('Primary Image URL', validators=[DataRequired()])
    submit = SubmitField('Save Product')