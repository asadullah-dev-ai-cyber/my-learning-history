from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], coerce=int, validators=[DataRequired()])
    title = StringField('Title', validators=[Length(max=120)])
    comment = TextAreaField('Review', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Submit Review')