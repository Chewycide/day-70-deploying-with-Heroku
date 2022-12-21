from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# LOGIN MANAGER
login_manager = LoginManager(app)


# GRAVATAR
gravatar = Gravatar(
    app,
    size=100,
    rating='g',
    default='retro',
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None
)


##CONFIGURE TABLES
class BlogPost(db.Model):
    """Database mode for blog posts"""
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    #Create Foreign Key, "users.id" the users refers to the tablename of User.
    # NOTE: the Foreign Key basically just refers to who is the author of the post
    # in this case the author_id references the id of the author who made the post.
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # author refers to the User class, when we say author.name
    # we are saying something like User.name, we can access the values of the
    # User model.
    # in short, author is now a User object
    author = relationship("User", back_populates="posts")
    # comments is a list of Comment object attached to 1 blog post (one-to-many relationship)
    comments = relationship("Comment", back_populates="parent_post")

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    

class User(UserMixin, db.Model):
    """Database model for users"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    # posts is a list of BlogPost objects attached to 1 user (one-to-many relationship)
    posts = relationship("BlogPost", back_populates="author")
    # comments is a list of Comment object attached to 1 user (one-to-many relationship)
    comments = relationship("Comment", back_populates="comment_author")


class Comment(db.Model):
    """Database model for user comments"""
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    # parent user
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_author = relationship("User", back_populates="comments")
    # parent blog post
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    parent_post = relationship("BlogPost", back_populates="comments")
    # String and Text difference is how many characters a user can input
    # String = 255 characters
    # Text = 30,000 characters
    text = db.Column(db.Text, nullable=False)


# USER LOADER CALLBACK
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ADMIN ONLY DECORATOR
def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # if user is not authenticated or not user id is not equal to 1
        # then, abort and raise response error 403 - forbidden
        if not current_user.is_authenticated or current_user.id != 1:

            return abort(403)

        # else continue
        return func(*args, **kwargs)

    return decorated_function


# ROUTES
@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=["POST", "GET"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        hashed_password = generate_password_hash(
            register_form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )

        # Add user to database
        new_user = User(
            name=register_form.name.data,
            email=register_form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        # auto login user after successful creation of account
        login_user(new_user)

        return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=register_form)


@app.route('/login', methods=["POST", "GET"])
def login():
    login_form = LoginForm()

    # validate and search for user on the database
    if login_form.validate_on_submit():
        user_query = User.query.filter_by(email=login_form.email.data).first()

        # check if user is in database and entered password matches password on the database
        if user_query and check_password_hash(user_query.password, login_form.password.data):
            login_user(user_query)
            return redirect(url_for('get_all_posts'))
        else:
            flash("User does not exist or Password Incorrect")
            return redirect(url_for('login'))

    return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["POST", "GET"])
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    comment_form = CommentForm()

    # validate user
    if comment_form.validate_on_submit():

        # check if user is logged in, if not then flash message and redirect to login page
        if not current_user.is_authenticated:
            flash("Please Login before commenting.")

            return redirect(url_for('login'))

        # else if user is authenticated, add new comment to database and show it to the post page
        new_comment = Comment(
            text = comment_form.comment.data,
            parent_post = requested_post,
            comment_author = current_user
        )
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('show_post', post_id=post_id))

    return render_template("post.html", post=requested_post, form=comment_form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=["POST", "GET"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>")
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()

        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)




