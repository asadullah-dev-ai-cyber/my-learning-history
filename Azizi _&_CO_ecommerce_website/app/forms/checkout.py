from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    shipping_address = StringField('Shipping Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])

    # Payment fields (Mock interface)
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=15, max=19)])
    card_expiry = StringField('Expiry (MM/YY)', validators=[DataRequired(), Length(min=5, max=5)])
    card_cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=4)])

    submit = SubmitField('Complete Purchase')