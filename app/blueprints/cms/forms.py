from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class ArticleForm(FlaskForm):
    title = StringField('Article Title', validators=[DataRequired(), Length(max=200)])
    summary = StringField('Summary', validators=[Length(max=500)], render_kw={"placeholder": "Brief description of the article"})
    content = TextAreaField('Content (HTML Supported)', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    tags = StringField('Tags', render_kw={"placeholder": "Comma-separated values, e.g. space, stars, galaxy"})
    image = FileField('Cover Image Upload', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')
    ])
    references_data = TextAreaField('Citations & References', render_kw={"placeholder": "One citation link/reference per line"})
    is_published = BooleanField('Publish Immediately')
    is_featured = BooleanField('Feature on Home Page')
    change_summary = StringField('Edit Reason / Version Comment', default='Updated article content', validators=[Length(max=255)])
    submit = SubmitField('Save Article')


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('Save Category')
