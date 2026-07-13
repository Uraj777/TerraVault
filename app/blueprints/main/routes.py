from flask import Blueprint, render_template, request, jsonify, current_app, Response, send_from_directory
from app.services.wiki_service import WikiService
from app.models.article import Category, Tag, Article
from app.extensions import db
import os

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


@main_bp.route('/health')
def health():
    """Health check endpoint for Render/hosting platforms."""
    db_status = "healthy"
    try:
        # Simple database ping
        db.session.execute(db.text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
        'database': db_status,
        'app': 'healthy'
    }), 200 if db_status == "healthy" else 500


@main_bp.route('/robots.txt')
def robots():
    """SEO robots.txt crawling configuration."""
    content = "User-agent: *\nAllow: /\nDisallow: /auth/profile/edit\nDisallow: /cms/\nSitemap: " + request.url_root + "sitemap.xml"
    return content, 200, {'Content-Type': 'text/plain'}


@main_bp.route('/sitemap.xml')
def sitemap():
    """SEO XML sitemap of all active articles."""
    pages = []
    # Add static pages
    pages.append({'loc': request.url_root, 'changefreq': 'daily', 'priority': '1.0'})
    pages.append({'loc': request.url_root + 'auth/login', 'changefreq': 'monthly', 'priority': '0.3'})
    pages.append({'loc': request.url_root + 'auth/register', 'changefreq': 'monthly', 'priority': '0.3'})
    
    # Add dynamic article pages
    try:
        articles = Article.query.filter_by(is_published=True).all()
        for art in articles:
            loc = request.url_root + 'wiki/' + art.slug
            pages.append({'loc': loc, 'changefreq': 'weekly', 'priority': '0.8'})
    except Exception:
        pass
        
    sitemap_xml = render_template('main/sitemap.xml', pages=pages)
    return Response(sitemap_xml, mimetype='application/xml')


@main_bp.route('/favicon.ico')
def favicon():
    """Serve favicon shortcut icons directly from static folder."""
    return send_from_directory(current_app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
