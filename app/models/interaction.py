from datetime import datetime
from app.extensions import db

class Media(db.Model):
    __tablename__ = 'media'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    mimetype = db.Column(db.String(100))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Media {self.filename}>"


class Draft(db.Model):
    __tablename__ = 'drafts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.String(500))
    content = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Draft {self.title}>"


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Composite unique constraint to avoid duplicate bookmarks
    __table_args__ = (db.UniqueConstraint('user_id', 'article_id', name='_user_article_bookmark_uc'),)
    
    def __repr__(self):
        return f"<Bookmark user_id={self.user_id} article_id={self.article_id}>"


class ReadingHistory(db.Model):
    __tablename__ = 'reading_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    time_spent = db.Column(db.Integer, default=0)  # in seconds
    last_viewed = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite unique constraint for history entries per user-article
    __table_args__ = (db.UniqueConstraint('user_id', 'article_id', name='_user_article_history_uc'),)
    
    def __repr__(self):
        return f"<ReadingHistory user_id={self.user_id} article_id={self.article_id}>"
