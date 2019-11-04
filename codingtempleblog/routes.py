from codingtempleblog import app, db
from flask import render_template, request, flash, redirect, url_for

# Import Forms
from codingtempleblog.forms import SignUpForm,LoginForm,PostForm

# Import Models 
from codingtempleblog.models import User, Post, check_password_hash

# Import Flask-Login Module/ functions
from flask_login import login_user, current_user, logout_user, login_required

import stripe

# Home route 
@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html",posts=posts)

@app.route("/register", methods=["GET","POST"])
def createUser():
    form = SignUpForm()
    if request.method == 'POST' and form.validate():
        flash("Thank you for signing up!")
        # Gathering Form Data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(username, email, password)

        # Add Form data to User Model Class
        user = User(username,email,password) 
        db.session.add(user) # Start communication with database
        db.session.commit() # Save Data to Database
        return redirect(url_for('login'))

    else:
        flash("Your form is missing some data")
    return render_template('register.html', register_form=form)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user_email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == user_email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            print(current_user.username)
            return redirect(url_for('home'))
    return render_template("login.html", login_form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/post', methods=["GET","POST"])
@login_required
def post():
    form = PostForm()
    title = form.title.data
    content = form.content.data
    user_id = current_user.id

    # Instantiate Post Class
    post = Post(title = title, content = content, user_id = user_id)
    db.session.add(post)
    db.session.commit()
    return render_template('post.html', post_form = form)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post = post)
    
@app.route('/payment',methods=['GET', 'POST'])
def payment():
    # Set your secret key: remember to change this to your life secret key in production
    # Set your keys here: http://dashboard.stripe.com/account/apikeys
    stripe.api_key = 'sk_test_9TeCZ25j0vTd08anOqF1kYK4'
    publishable_key = 'pk_test_MYb13ldDgVSh5P07dt9rLUG400S28azhpY'
    price = 5000

    return render_template('payment.html', key=publishable_key, price=price)