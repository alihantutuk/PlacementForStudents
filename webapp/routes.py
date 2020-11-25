from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from webapp import app, db, bcrypt
from webapp.forms import RegistrationForm, LoginForm
from webapp.db_models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
#from webapp.db_models import Img
from base64 import b64encode






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


@app.route( "/" )
@app.route( "/home" )
def home():
    return render_template( 'home.html', posts=posts )


@app.route( "/about" )
def about():
    return render_template( 'about.html', title='About' )


@app.route( "/account/" )
@login_required  # from flask_login package
def account():

    if current_user.type == False:  # if it is company
        return redirect( url_for( 'account2', username=current_user.username ) )

    # if it is user --> userprofile redirect


@app.errorhandler( 404 )
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template( '404.html' ), 404


@app.route( "/company/<username>" )
def account2(username):
    user = User.query.filter_by( username=username ).first()
    if user is not None and user.type == False:  # if it is company #check if details is completed
        return render_template( 'account_company.html', user=user )
    else:
        abort( 404, description="Resource not found" )
        return render_template( '404.html' )


@app.route( "/register", methods=['GET', 'POST'] )
def register():
    if current_user.is_authenticated:
        return redirect( url_for( 'home' ) )

    form = RegistrationForm()

    # came from posted form, if validated
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash( form.password.data ).decode( 'utf-8' )
        user = User( username=form.username.data, email=form.email.data, password=hashed_password )
        db.session.add( user )
        db.session.commit()
        flash( f'Account created for {form.username.data}!', 'success' )
        return redirect( url_for( 'login' ) )

    return render_template( 'register.html', title='Register', form=form )


@app.route( "/login", methods=['GET', 'POST'] )
def login():
    if current_user.is_authenticated:
        return redirect( url_for( 'home' ) )

    form = LoginForm()

    # came from posted form, if validated including database.
    if form.validate_on_submit():


        user = User.query.filter_by( email=form.email.data ).first()
        print("User : ",user)


        if user and bcrypt.check_password_hash( user.password, form.password.data ):

            login_user( user, remember=form.remember.data )

            # from where login page is reached
            next_page = request.args.get( 'next' )
            if next_page:
                return redirect( next_page )  # url_for or pure string?
            else:
                return redirect( url_for( 'home' ) )
        else:
            flash( 'Login Unsuccessful. Please check username and password', 'danger' )
    return render_template( 'login.html', title='Login', form=form )


@app.route( "/logout" )
def logout():
    logout_user()  # from flask_login package
    return redirect( url_for( 'home' ) )


@app.route("/search")
def search():
    username = request.args.get( 'name' )
    users = User.query.filter(User.username.ilike(username+"%")).all()

    companies = []
    students = []
    for u in users:
        if u.type:
            students.append(u)
        else:
            companies.append(u)

    return render_template('searchresults.html',students = students,companies = companies)






#Image upload show part
"""
@app.route( '/upload', methods=['POST'] )
def upload():
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename( pic.filename )
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Img( img=pic.read(), name=filename, mimetype=mimetype )
    db.session.add( img )
    db.session.commit()

    return 'Img Uploaded!', 200


@app.route( '/<int:id>' )
def get_img(id):
    obj = Img.query.filter_by( id=id ).first()
    image = b64encode( obj.img ).decode( "utf-8" )
    if not obj.img:
        return 'Img Not Found!', 404

    return render_template( "show.html", obj=obj, image=image )


@app.route( '/up' )
def up():
    return render_template( "imageup.html" )
"""

