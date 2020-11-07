from flask import render_template, url_for, flash, redirect, request
from webapp import app, db, bcrypt
from webapp.forms import RegistrationForm, LoginForm
#from webapp.db_models import User,Post
from flask_login import login_user,current_user,logout_user,login_required



posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/account")
@login_required #from flask_login package
def account():
    return render_template('account.html', title='Account')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect( url_for( 'home' ))

    form = RegistrationForm()

    #came from posted form, if validated
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash( form.password.data ).decode( 'utf-8' )
        user = User(username=form.username.data, email=form.email.data, password=hashed_password )
        db.session.add( user )
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect( url_for( 'home' ))

    form = LoginForm()

    #came from posted form, if validated including database.
    if form.validate_on_submit():
        user = User.query.filter_by( email=form.email.data ).first()
        if user and bcrypt.check_password_hash( user.password, form.password.data ):
            
            login_user( user, remember=form.remember.data)

            #from where login page is reached
            next_page = request.args.get( 'next' )
            if next_page:
                return redirect(next_page) # url_for or pure string?
            else:
                return redirect( url_for( 'home' ) )
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user() #from flask_login package
    return redirect(url_for('home'))