"""SQLAlchemy models for blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://images.playground.com/a661ca20af4f470fb849633237890d85.jpeg"

def connect_db(app):
  db.app = app
  db.init_app(app)

#MODEL GO BELOW!

class User(db.Model):
  """User model"""

  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.Text, nullable=False)
  last_name = db.Column(db.Text, nullable=False)
  image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

  @property
  def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"