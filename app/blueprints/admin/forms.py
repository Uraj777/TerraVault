from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class AdminLoginForm(FlaskForm):
    username = StringField('Admin Username or Email', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Access Control Center')

class ArticleForm(FlaskForm):
    title = StringField('Article Title', validators=[DataRequired(), Length(max=200)])
    summary = StringField('Summary', validators=[Length(max=500)], render_kw={"placeholder": "Brief description of the article"})
    content = TextAreaField('Content (HTML Supported)', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    tags = StringField('Tags', render_kw={"placeholder": "Comma-separated values, e.g. history, space, volcano"})
    image = FileField('Cover Image Upload', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')
    ])
    references_data = TextAreaField('Citations & References', render_kw={"placeholder": "One citation link/reference per line"})
    status = SelectField('Publish Status', choices=[
        ('draft', 'Draft (Unpublished)'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], default='draft')
    is_featured = BooleanField('Feature on Home Page')
    change_summary = StringField('Edit Reason / Version Comment', default='Updated article content', validators=[Length(max=255)])
    submit = SubmitField('Save Article')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('Save Category')
