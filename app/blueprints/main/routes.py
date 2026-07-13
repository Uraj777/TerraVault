from flask import Blueprint, render_template, request
from app.services.wiki_service import WikiService
from app.models.article import Category, Tag

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Renders the main catalog home page, featured articles, and recent publications."""
    featured = WikiService.get_featured_articles()
    recent = WikiService.get_all_published_articles(limit=6)
    categories = WikiService.get_all_categories()
    
    return render_template('main/home.html', featured=featured, recent=recent, categories=categories)


@main_bp.route('/search')
def search():
    """Global search across articles."""
    query = request.args.get('q', '').strip()
    results = []
    if query:
        results = WikiService.search_articles(query)
    return render_template('main/search.html', query=query, results=results)


@main_bp.route('/category/<slug>')
def category(slug):
    """Renders articles filtered by a specific category."""
    cat = Category.query.filter_by(slug=slug).first_or_404()
    articles = WikiService.get_all_published_articles(category_id=cat.id)
    return render_template('main/category.html', category=cat, articles=articles)


@main_bp.route('/tag/<slug>')
def tag(slug):
    """Renders articles filtered by a specific tag."""
    tag_obj = Tag.query.filter_by(slug=slug).first_or_404()
    articles = WikiService.get_all_published_articles(tag_id=tag_obj.id)
    return render_template('main/tag.html', tag=tag_obj, articles=articles)
