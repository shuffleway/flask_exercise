from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chinkljkdhkhdjgjdhhwkhdhkshkhdd"
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect('/users')

@app.route('/users')
def list_users():
    users = User.query.all()

    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user = User(
            first_name=request.form.get('first_name', ''),
            last_name=request.form.get('last_name', ''),
            image_url=request.form.get('image_url') or None
        )

        db.session.add(new_user)
        db.session.commit()

        return render_template('users/index.html', users=User.query.all())

    return render_template('users/new.html')

@app.route('/users/<int:id>')
def user_profile(id):
    user = User.query.get_or_404(id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:id>/edit')
def edit_user(id):
    user = User.query.get_or_404(id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:id>/delete', methods=["POST"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

