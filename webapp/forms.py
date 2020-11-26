from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from webapp.db_models import User
from flask_login import current_user
from webapp import bcrypt



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # db validation for uniqueness in form
    def validate_username(self, username):
        user = User.query.filter_by( username=username.data ).first()
        if user:
            raise ValidationError( 'That username is taken. Please choose a different one.' )

    # db validation for uniqueness in form
    def validate_email(self, email):
        user = User.query.filter_by( email=email.data ).first()
        if user:
            raise ValidationError( 'That email is taken. Please choose a different one.' )


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CompanyEditForm(FlaskForm):
    username = StringField( 'Username',
                            validators=[DataRequired(), Length( min=2, max=20 )] )
    email = StringField( 'Email',validators=[DataRequired(), Email()] )
    password = PasswordField( 'Password', validators=[DataRequired()] )
    confirm_password = PasswordField( 'Confirm Password',
                                      validators=[DataRequired(), EqualTo( 'password' )] )
    website = StringField( 'Website' )
    linkedin = StringField( 'Linkedin')
    github = StringField( 'GitHub')
    name = StringField('Name')
    address = StringField('Address')
    image = FileField( 'Image', validators=[FileAllowed( ['jpg', 'png'] )] )
    description = StringField('description',validators=[DataRequired()])
    sector = StringField( 'sector', validators=[DataRequired()] )
    numberofworkers = IntegerField('numberofworkers',validators=[DataRequired()])
    submit = SubmitField( 'Update' )

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by( username=username.data ).first()
            if user:
                raise ValidationError( 'That username is taken. Please choose a different one.' )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by( email=email.data ).first()
            if user:
                raise ValidationError( 'That email is taken. Please choose a different one.' )

    def validate_password(self,password):

        if bcrypt.check_password_hash( current_user.password, password.data ) == False:
            raise ValidationError( 'That password does not belong to this account' )



