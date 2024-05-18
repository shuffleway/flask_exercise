"""SQLAlchemy models for blogly."""

from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://images.playground.com/a661ca20af4f470fb849633237890d85.jpeg"

def connect_db(app):
  db.app = app
  db.init_app(app)

#MODEL GO BELOW!

class User(db.Model):
    """Site User"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Blog Post"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class Tag(db.Model):
    """Tag that can be added to posts."""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)


class PostTag(db.Model):
    """Tag on a post."""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


