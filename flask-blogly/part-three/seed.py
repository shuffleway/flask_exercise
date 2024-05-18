"""Seed file to make sample data for db"""

from app import app
from models import db, connect_db, User, Post, Tag, PostTag
import datetime

# Drop all tables and recreate them
db.drop_all()
db.create_all()

# Add sample users
u1 = User(first_name='Juan', last_name='Mercy')
u2 = User(first_name='Jenny', last_name='Nancy')
u3 = User(first_name='keniaso', last_name='bugly', image_url='https://img.freepik.com/premium-photo/beauty-body-sexy-woman-photo-ai-generated_980993-3401.jpg')

db.session.add_all([u1, u2, u3])
db.session.commit()

# Add sample posts
p1 = Post(title="Twins sister is here", content="Twin sister came back since last week, you did not even see her", user=u2)
p2 = Post(title="Jericho has fallen", content="God's children shouted, the walls fell down flat", user=u1)
p3 = Post(title="Daniel doesn't even know", content="Some people mess with the wrong people and fall in trouble for that.", user=u3)

db.session.add_all([p1, p2, p3])
db.session.commit()

# Add sample tags
t1 = Tag(name='computer')
t2 = Tag(name='recent news')
t3 = Tag(name='phones')
t4 = Tag(name='new products')
t5 = Tag(name='fun_night')

db.session.add_all([t1, t2, t3, t4, t5])
db.session.commit()

# Associate tags with posts
pt1 = PostTag(post_id=p1.id, tag_id=t2.id)
pt2 = PostTag(post_id=p2.id, tag_id=t3.id)
pt3 = PostTag(post_id=p3.id, tag_id=t5.id)

db.session.add_all([pt1, pt2, pt3])
db.session.commit()
