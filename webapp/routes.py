from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from webapp import app, db, bcrypt
from webapp.forms import RegistrationForm, LoginForm, CompanyEditForm, CompanyCreateForm, StudentCreateForm
from webapp.db_models import User,Companydetail,Advertisement, Studentdetail,Interestarea, Keyword, advertisement_keyword
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
#from webapp.db_models import Img
from base64 import b64encode
from webapp.util import get_interests,get_business_keywords






posts = [
    {
        'id' : '1',
        'company': 'Mono Analytics',
        'title': 'Data Science',
        'description': 'First post content lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor'
                       'lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor'
                       'lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor',
        'date_posted': 'April 20, 2018',
        'deadline'    : 'July 24, 2019',
        'keywords': ["python","java","c++","Office","SQL","machine learning","HTML",\
                     "deep learning","computer vision","C","Data structures","Object Oriented Programming"]
    },
    {
        'id' : '2',
        'company': 'Baykar',
        'title': 'Flight Designer',
        'description': 'Second post content',
        'date_posted': 'April 21, 2018',
        'deadline'    : 'May 05, 2018',
        'keywords': ["Autocad","Solid Works","c","Management"]
    },
    {
        'id' : '3',
        'company': 'Cezeri',
        'title': 'Artificial Intelligence engineer',
        'description': 'First post content',
        'date_posted': 'January 26, 2018',
        'deadline'    : 'July 26, 2018',
        'keywords': ["python","machine learning","HTML",\
                     "deep learning","computer vision","C","Data structures","Object Oriented Programming"]
    },
    {
        'id' : '4',
        'company': 'Tübitak',
        'title': 'Product Designer',
        'description': 'Second post content',
        'date_posted': 'April 21, 2018',
        'deadline'    : 'May 05, 2018',
        'keywords': ["python","Solid Works","c++","Management"]
    },
    {
        'id' : '5',
        'company': 'Tübitak',
        'title': 'Software Engineer',
        'description': 'First post content',
        'date_posted': 'January 21, 2018',
        'deadline'    : 'September 05, 2018',
        'keywords': ["c++","Data structures","c","Management"]
    },
    {
        'id' : '6',
        'company': 'Baykar',
        'title': 'Software Engineer',
        'description': 'First post content',
        'date_posted': 'February 02, 2018',
        'deadline'    : 'March 02, 2018',
        'keywords': ["c++","Data structures","c","java","css","deep learning"]
    }
]



@app.route( "/",methods=['GET', 'POST'] )
@app.route( "/home",methods=['GET', 'POST'] )
def home():
    filtered= ''
    if request.method=='POST':

        search_result =request.form.get("search_area")
        selection = request.form.get("selection")
        #TODO: will be connected to the database
        selected=[]

        print(selection)
        if search_result:
            if selection == "company":
                for post in posts:
                    if search_result in post["company"]:
                        selected.append(post)
            elif selection == "title":
                for post in posts:
                    if search_result in post["title"]:
                        selected.append(post)
            else:
                for post in posts:
                    for key in post["keywords"]:
                        if search_result in key:
                            selected.append(post)
                filtered=search_result

        if selected == []:
            flash("No company found for your search...", "danger")
        else:
            return render_template('home.html', posts=selected,filter_keyword=filtered)

    advertisement = Advertisement.query.all()
    posts = []
    for adv in advertisement:
        post = {}
        print(adv.companydetail_id)
        post['company'] = Companydetail.query.filter_by(id=adv.companydetail_id).first().name
        post['title'] = adv.title
        post['description'] = adv.description
        post['deadline'] = adv.deadline
        post['date_posted'] = adv.date_posted
        user_id=Companydetail.query.filter_by(id=adv.companydetail_id).first().user_id
        user_name=User.query.filter_by(id=user_id).first().username
        post["username"]=user_name
        keys = []
        keyword_adv = db.session.query(advertisement_keyword).filter_by(advertisement_id=adv.id).all()

        for k_id in keyword_adv:
            key = Keyword.query.filter_by(id=k_id[1]).first().name
            keys.append(key)
        post["keywords"] = keys
        posts.append(post)

    return render_template('home.html', posts=posts)

@app.route( "/<keyword>",methods=['GET','POST'] )
def keywords(keyword):
    if request.method=='GET':
        # TODO: will be connected to the database
        filtered=[]
        for post in posts:
            for key in post["keywords"]:
                if key==keyword:
                    filtered.append(post)
        return render_template("home.html",posts=filtered,filter_keyword=keyword)
    else:
        flash(f"No method allowed for /{keyword} page...", "danger")
        return render_template("home.html", posts=posts, filter_keyword='')

@app.route( "/detail",methods=['GET'] )
def ad_detail():
    advertisement=Advertisement.query.all()
    posts=[]
    for adv in advertisement:
        post={}
        print(adv.companydetail_id)
        post['company']=Companydetail.query.filter_by(id =adv.companydetail_id).first().name
        post['title'] = adv.title
        post['description'] = adv.description
        post['deadline']=adv.deadline
        post['date_posted'] = adv.date_posted

        keys=[]
        keyword_adv=db.session.query(advertisement_keyword).filter_by(advertisement_id=adv.id).all()

        for k_id in keyword_adv:
            key=Keyword.query.filter_by(id=k_id[1]).first().name
            keys.append(key)
        post["keywords"]=keys
        posts.append(post)




    return render_template("ad_detail.html",posts=posts)







@app.route( "/about" )
def about():
    return render_template( 'about.html', title='About' )


@app.route( "/create_profile" )
def create_profile():
    editform = CompanyCreateForm()
    editform_student = StudentCreateForm()
    return render_template( 'create_profile.html', title='Create Profile', form=editform, form_student=editform_student)


@app.route( "/create_profile_student", methods=['POST'])
def create_profile_student():
    editform_student = StudentCreateForm()
    if request.method == 'POST':
        if editform_student.validate_on_submit():

            student_detail = Studentdetail()
            student_detail.user_id = current_user.id

            student_detail.name_surname = editform_student.name.data
            student_detail.university = editform_student.university.data
            student_detail.class_level = editform_student.class_level.data
            student_detail.gpa = editform_student.gpa.data
            student_detail.active = editform_student.active.data
            student_detail.github = editform_student.github.data
            student_detail.linkedin = editform_student.linkedin.data



            # get image
            image = editform_student.image.data
            if image:
                filename = secure_filename(image.filename)
                mimetype = image.mimetype

                student_detail.img = b64encode(image.read()).decode("utf-8")
                student_detail.imgname = filename
                student_detail.mimetype = mimetype

            try:
                db.session.add(student_detail)
                current_user.complete = True
                current_user.type = True
                db.session.add(current_user)
                db.session.commit()


                print("success")
            except AssertionError as err:
                db.session.rollback()
                print("rollback")

            return redirect(url_for('account', username=current_user.username))
        else:
            return redirect(url_for('account', username=current_user.username))

    return render_template( 'create_profile.html', title='Create Profile', form=editform_student)


@app.route( "/create_profile_company", methods=['POST'])
def create_profile_company():
    editform = CompanyCreateForm()
    if request.method == 'POST':
        if editform.validate_on_submit():

            company_details = Companydetail()
            company_details.user_id = current_user.id

            company_details.name = editform.name.data
            company_details.description = editform.description.data
            company_details.address = editform.address.data
            company_details.linkedin = editform.linkedin.data
            company_details.github = editform.github.data
            company_details.website = editform.website.data
            company_details.numberofworkers = editform.numberofworkers.data
            company_details.sector = editform.sector.data

            print(company_details)

            # get image
            image = editform.image.data
            if image:
                filename = secure_filename(image.filename)
                mimetype = image.mimetype

                company_details.img = b64encode(image.read()).decode("utf-8")
                company_details.imgname = filename
                company_details.mimetype = mimetype

            try:
                db.session.add(company_details)
                current_user.complete = True
                current_user.type = False
                db.session.add(current_user)
                db.session.commit()


                print("success")
            except AssertionError as err:
                db.session.rollback()
                print("rollback")

            return redirect( url_for( 'account2', username=current_user.username ) )
        else:
            return redirect(url_for('account', username=current_user.username))

    return render_template( 'create_profile.html', title='Create Profile', form=editform)


@app.route( "/account/" )
@login_required  # from flask_login package
def account():

    if current_user.complete == False:
        return redirect(url_for('create_profile'))

    if current_user.type == False:  # if it is company
        return redirect( url_for( 'account2', username=current_user.username ) )
    else: # if it is student
        # TODO, because studend page is in development, i show 404 error until the development ends
        # TODO developer of the student page should change here after the development ends.
        abort(404, description="Student page does not exist")
        return render_template('404.html')

    # if it is user --> userprofile redirect


@app.errorhandler( 404 )
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template( '404.html' ), 404


@app.route( "/company/<username>",methods=['GET', 'POST'])
def account2(username):
    user = User.query.filter_by( username=username ).first()
    if user is not None and user.type == False:  # if it is company #check if details is completed
        ads = user.company_details.advertisements
        ads_sorted  = sorted(ads, key=lambda x: x.date_posted, reverse=True)
        img_data = user.company_details.img
        business_keywords = get_business_keywords(user)

        editform = CompanyEditForm()


        if request.method == 'POST':
            if editform.validate_on_submit():

                # Only current user can do editing, so I am changing currentuser.
                hashed_password = bcrypt.generate_password_hash( editform.password.data ).decode( 'utf-8' )
                current_user.username = editform.username.data
                current_user.email = editform.email.data
                current_user.company_details.name = editform.name.data
                current_user.company_details.description = editform.description.data
                current_user.company_details.address = editform.address.data
                current_user.company_details.linkedin = editform.linkedin.data
                current_user.company_details.github = editform.github.data
                current_user.company_details.website = editform.website.data
                current_user.company_details.numberofworkers = editform.numberofworkers.data
                interests = get_interests(editform.sector.data,current_user.company_details.id)
                if len(interests)>0:current_user.company_details.interests.extend(interests)
                #there can be max 4 elements in interests
                if len(interests) > 4:current_user.company_details.interests = current_user.company_details.interests[0:4]



                #get image
                image = editform.image.data
                if image:
                    filename = secure_filename(image.filename )
                    mimetype = image.mimetype

                    current_user.company_details.img = b64encode(image.read()).decode("utf-8")
                    current_user.company_details.imgname = filename
                    current_user.company_details.mimetype = mimetype





                try:
                    db.session.add(current_user)
                    db.session.commit()
                except AssertionError as err:
                    db.session.rollback()
                    print("rollback")

                ads = current_user.company_details.advertisements
                ads_sorted = sorted( ads, key=lambda x: x.date_posted, reverse=True )
                img_data = current_user.company_details.img
                return render_template( 'account_company.html', user=current_user, ads = ads_sorted, form = editform, formerror = False, img_data = img_data, business_keywords = business_keywords)
            else:
                return render_template( 'account_company.html', user=user, ads=ads_sorted, form=editform, formerror = True, img_data = img_data, business_keywords = business_keywords)


        return render_template( 'account_company.html', user=user, ads = ads_sorted, form = editform, formerror = False, img_data = img_data, business_keywords = business_keywords)
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


@app.route("/deleteinterest")
def delete_interest():
    company_detail_id = int(request.args.get('company_detail_id'))
    interest_id = int(request.args.get('interest_id'))


    company_detail_entity = Companydetail.query.filter_by(id = company_detail_id).first()
    if company_detail_entity:
        new_interests = []
        for i in company_detail_entity.interests:
            if i.id == interest_id:
                continue
            new_interests.append(i)
        company_detail_entity.interests = new_interests

    try:
        db.session.add(company_detail_entity)
        db.session.commit()
    except AssertionError as err:
        db.session.rollback()



    return redirect(url_for('account2',username = company_detail_entity.user.username))

