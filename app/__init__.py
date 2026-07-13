import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
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
    
    return app


def register_blueprints(app):
    """Register all application blueprints."""
    from app.blueprints.main.routes import main_bp
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.wiki.routes import wiki_bp
    from app.blueprints.cms.routes import cms_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(wiki_bp, url_prefix='/wiki')
    app.register_blueprint(cms_bp, url_prefix='/cms')


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
