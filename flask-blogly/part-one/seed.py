"""Seed file to make sample data for db"""

from models import db, User, DEFAULT_IMAGE_URL
from app import app

#Create all tables
db.drop_all()
db.create_all()

#add sample users
u1 = User(first_name='Juan', last_name='Mercy')
u2 = User(first_name='Jenny', last_name='Nancy')
u3 = User(first_name='keniaso', last_name='bugly', image_url = 'https://img.freepik.com/premium-photo/beauty-body-sexy-woman-photo-ai-generated_980993-3401.jpg')

db.session.add_all([u1, u2, u3])
db.session.commit()

