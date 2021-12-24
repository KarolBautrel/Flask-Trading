from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField  

from wtforms.validators import Length, EqualTo , Email, DataRequired, ValidationError
from market.models import User



class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[Length(min=3, max=20), DataRequired()])
    email = StringField(label="Email", validators=[Email(),DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label="Create Account")


    def validate_username(self,username_to_check):
           
        user = User.query.filter_by(username = username_to_check.data).first()
        if user: 
            raise ValidationError ('Username already exists')

    def validate_email(self,email_to_check):
        email = User.query.filter_by(email_address = email_to_check.data).first()
        if email:
            raise ValidationError ('Email already exists')


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase")

class SellingItemForm(FlaskForm):
    submit = SubmitField(label="Sell")
<<<<<<< HEAD


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(label="Old Password", validators=[DataRequired()])
    new_password = PasswordField(label="New Password", validators=[Length(min=6),DataRequired()])
    new_password2 = PasswordField(label="Confirm new password", validators=[EqualTo('new_password'),DataRequired()])
    submit = SubmitField(label="Change Password")

class ChangeEmailForm(FlaskForm):
    email = StringField(label="Email", validators=[Email(),DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=6),DataRequired()])
    submit = SubmitField(label="Change Email")
=======
>>>>>>> 464e3851055ee4ec4434ce378bf394d1472c8f6d
