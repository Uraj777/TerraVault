import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_talisman import Talisman
from flask_compress import Compress
from whitenoise import WhiteNoise
from app.config import config_by_name
from app.extensions import db, migrate, login_manager, csrf

def create_app(config_name=None):
    """Application Factory Pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
        
    # Set explicit root paths for template and static folders
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(root_dir, 'templates')
    static_dir = os.path.join(root_dir, 'static')
        
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))
    
    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Setup logging
    setup_logging(app)
    
    # Register User Loader for Flask-Login
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # Register blueprints
    register_blueprints(app)
    
    # Register global error handlers
    register_error_handlers(app)
    
    # Global context processors and custom Jinja filters
    register_context_processors(app)
    
    # Custom Content Security Policy supporting Bootstrap 5 and FontAwesome CDNs plus inline scripts
    csp = {
        'default-src': [
            '\'self\'',
            'https://cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com',
        ],
        'script-src': [
            '\'self\'',
            '\'unsafe-inline\'', # Required for Chart.js & Dark Mode toggler scripts
            'https://cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com',
        ],
        'style-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'https://cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com',
            'https://fonts.googleapis.com',
        ],
        'font-src': [
            '\'self\'',
            'https://fonts.gstatic.com',
            'https://cdnjs.cloudflare.com',
        ],
        'img-src': [
            '\'self\'',
            'data:',
            'https://images.unsplash.com',
            'https://upload.wikimedia.org',
        ]
    }
    
    # Enforce Talisman security headers (HTTP Strict Transport Security, XSS protections, frame guards)
    # Require HTTPS only if in production mode
    is_prod = (config_name == 'production' or os.environ.get('FLASK_ENV') == 'production')
    Talisman(app, content_security_policy=csp, force_https=is_prod)
    
    # Enable Gzip and Brotli compression for server responses
    Compress(app)
    
    # Wrap WSGI pipeline with WhiteNoise to serve static assets with far-future caching headers
    app.wsgi_app = WhiteNoise(app.wsgi_app, root=static_dir, prefix='static/')
    
    # Register anonymous visitor cookies & metrics logging
    register_request_handlers(app)
    
    return app


def register_request_handlers(app):
    import uuid
    import hashlib
    from datetime import datetime
    from flask import g, request
    from app.models.community import AnonymousVisitor, PageViewMetric
    from app.models.article import Article

    @app.before_request
    def before_request_func():
        # Skip static assets, health check, robots.txt, sitemap, favicon
        path = request.path
        if (path.startswith('/static/') or 
            path == '/health' or 
            path == '/favicon.ico' or 
            path == '/robots.txt' or 
            path == '/sitemap.xml'):
            g.visitor = None
            return
            
        anon_cookie = request.cookies.get('anon_explorer_id')
        cookie_to_set = None
        if not anon_cookie:
            anon_cookie = str(uuid.uuid4())
            g.set_anon_cookie = anon_cookie
            cookie_to_set = anon_cookie
        else:
            g.set_anon_cookie = None
            
        # Fetch or create AnonymousVisitor
        visitor = AnonymousVisitor.query.filter_by(uuid=anon_cookie).first()
        if not visitor:
            # Generate name based on UUID prefix
            short_id = anon_cookie[:4].upper()
            display_name = f"Anonymous Explorer #{short_id}"
            
            # Generate colorful avatar background based on hash
            h = int(hashlib.md5(anon_cookie.encode('utf-8')).hexdigest(), 16)
            hue = h % 360
            avatar_color = f"hsl({hue}, 70%, 45%)"
            
            visitor = AnonymousVisitor(
                uuid=anon_cookie,
                display_name=display_name,
                avatar_color=avatar_color
            )
            db.session.add(visitor)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                # Query again in case of concurrent writes
                visitor = AnonymousVisitor.query.filter_by(uuid=anon_cookie).first()
        else:
            # Update last seen timestamp
            visitor.last_seen_at = datetime.utcnow()
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                
        # Set on global context
        g.visitor = visitor
        
        # Track page view metrics selectively
        article_id = None
        if path.startswith('/wiki/'):
            slug = path.split('/wiki/')[-1]
            article = Article.query.filter_by(slug=slug).first()
            if article:
                article_id = article.id
                
        metric = PageViewMetric(
            path=path,
            article_id=article_id,
            visitor_uuid=visitor.uuid if visitor else None
        )
        db.session.add(metric)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    @app.after_request
    def after_request_func(response):
        if hasattr(g, 'set_anon_cookie') and g.set_anon_cookie:
            # 1 year long-lived secure browser cookie
            response.set_cookie(
                'anon_explorer_id',
                g.set_anon_cookie,
                max_age=365 * 24 * 60 * 60,
                httponly=True,
                samesite='Lax',
                secure=(os.environ.get('FLASK_ENV') == 'production')
            )
        return response


def register_blueprints(app):
    """Register all application blueprints."""
    from app.blueprints.main.routes import main_bp
    from app.blueprints.wiki.routes import wiki_bp
    from app.blueprints.admin.routes import admin_bp
    from app.blueprints.community.routes import community_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(wiki_bp, url_prefix='/wiki')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(community_bp, url_prefix='/c')


def register_error_handlers(app):
    """Register HTTP error handlers."""
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500


def register_context_processors(app):
    """Register custom filters and context variables."""
    # Custom filters
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%b %d, %Y'):
        if value is None:
            return ""
        return value.strftime(format)

    # Inject categories list into templates for navbar dropdowns
    from app.models.article import Category
    @app.context_processor
    def inject_categories():
        try:
            categories = Category.query.all()
        except Exception:
            categories = []
        return dict(nav_categories=categories)


def setup_logging(app):
    """Configure system logging rotating files."""
    if not app.debug and not app.testing:
        # Log to file in production
        os.makedirs('logs', exist_ok=True)
        file_handler = RotatingFileHandler('logs/terravault.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('TerraVault Startup')
    else:
        # Stdout logging for development
        logging.basicConfig(level=logging.INFO)
