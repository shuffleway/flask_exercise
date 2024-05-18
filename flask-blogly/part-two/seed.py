"""Seed file to make sample data for db"""

from models import db, User, Post, DEFAULT_IMAGE_URL
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

p1 = Post(title="Twins sister is here", content="Twin sister came back since last wee, you did not even see her", user_id=2)
p2 = Post(title="Jerico has fallen", content="God's children shouted, the walls fell down flat", user_id=1)
p3 = Post(title="Daniel don't even know", content="Some people mess with the wrong people and fall in trouble for that. ", user_id=3)

db.session.add_all([p1, p2, p3])
db.session.commit()