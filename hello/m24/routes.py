from flask import  render_template,url_for,flash , redirect 
from m24 import app , db , bcrypt
from m24.forms import RegistrationForm,  LoginForm , PostForm , AnonymousForm
from m24.models import User , Post , Anonymous
from flask_login import login_user, current_user , logout_user , login_required

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    anonymous = Anonymous.query.all()
    return render_template('home.html', posts=posts,anonymous=anonymous)

@app.route("/play")
def play():
    anonymous = Anonymous.query.all()
    return render_template('play.html', anonymous=anonymous)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route("/account")
@login_required
def account():
    return render_template('account.html')



@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html',form=form)


@app.route("/anonymous", methods=['GET', 'POST'])
@login_required
def anonymous_post():
    form = AnonymousForm()
    if form.validate_on_submit():
        anonymous = Anonymous(title=form.title.data, content=form.content.data)
        db.session.add(anonymous)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for("home"))    
    return render_template('lalu.html',form=form)
