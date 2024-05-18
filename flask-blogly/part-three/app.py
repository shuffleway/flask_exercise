from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from forms import PostForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chinkljkdhkhdjgjdhhwkhdhkshkhdd"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

##############################################################
#User profile
##############################################################
@app.route('/users')
def list_users():
    users = User.query.all()

    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Validate input data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        image_url = request.form.get('image_url')

        if not first_name or not last_name:
            flash('First name and last name cannot be empty.')
            return render_template('users/new.html')

        # Proceed with creating a new user if validation passes
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            image_url=image_url or None
        )

        db.session.add(new_user)
        db.session.commit()
        flash(f"User {new_user.full_name} added.")

        return render_template('users/index.html', users=User.query.all())

    # Display the form for adding a new user
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
    
    # Retrieve form data
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    # Validate input data
    if not first_name or not last_name:
        flash('First name and last name cannot be empty.', 'error')
        return redirect(f'/users/{user_id}/edit')

    # Update user details if validation passes
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url or user.image_url  # Preserve existing image_url if new one is not provided

    db.session.commit()
    flash(f"User {user.full_name} edited.", 'success')

    return redirect("/users")

@app.route('/users/<int:id>/delete', methods=["POST"])
def delete_user(id):
    user = User.query.get_or_404(id)
    # First, delete any tags associated with the user's posts
    PostTag.query.filter(PostTag.post_id.in_(
        db.session.query(Post.id).filter_by(user_id=id)
    )).delete(synchronize_session=False)
    # Then, delete the user's posts
    Post.query.filter_by(user_id=id).delete(synchronize_session=False)
    # Finally, delete the user
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.", 'success')
    return redirect('/users')



##############################################################
#POST / Articles
############################################################## 
@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    # Retrieve form data
    title = request.form.get('title')
    content = request.form.get('content')

    # Validate input data
    if not title:
        flash('Title input cannot be empty.', 'error')
        return redirect(f'/users/{user_id}/posts/new')
    elif not content:
        flash('content input cannot be empty.', 'error')
        return redirect(f'/users/{user_id}/posts/new')

    # Create a new post if validation passes
    new_post = Post(title=title,
                    content=content,
                    user=user, tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")






@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.", 'success')

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.", 'success')

    return redirect(f"/users/{post.user_id}")


##############################################################
#tags - post_tags
##############################################################

@app.route('/tags')
def tags_index():
    """Show a page with info on all tags."""
    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag."""
    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)

@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag."""
    name = request.form['name'].strip()
    if not name:
        flash("Tag name cannot be empty.", 'error')
        return redirect('/tags/new')

    post_ids = request.form.getlist("posts")
    if not post_ids:
        flash("At least one post must be selected.", 'error')
        return redirect('/tags/new')

    post_ids = [int(num) for num in post_ids if num.isdigit()]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()

    try:
        new_tag = Tag(name=name, posts=posts)
        db.session.add(new_tag)
        db.session.commit()
        flash(f"Tag '{new_tag.name}' added.", 'success')
    except IntegrityError:
        db.session.rollback()
        flash("An error occurred while adding the tag.", 'error')

    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag."""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag."""
    tag = Tag.query.get_or_404(tag_id)
    name = request.form['name'].strip()
    if not name:
        flash("Tag name cannot be empty.", 'error')
        return redirect(f'/tags/{tag_id}/edit')

    post_ids = request.form.getlist("posts")
    post_ids = [int(num) for num in post_ids if num.isdigit()]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    tag.name = name

    try:
        db.session.commit()
        flash(f"Tag '{tag.name}' edited.", 'success')
    except IntegrityError:
        db.session.rollback()
        flash("An error occurred while updating the tag.", 'error')

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag."""
    tag = Tag.query.get_or_404(tag_id)
    try:
        db.session.delete(tag)
        db.session.commit()
        flash(f"Tag '{tag.name}' deleted.", 'success')
    except IntegrityError:
        db.session.rollback()
        flash("An error occurred while deleting the tag.", 'error')

    return redirect("/tags")