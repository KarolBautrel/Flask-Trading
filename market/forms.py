from flask_wtf import FlaskForm
# zaimportowanie specjalnych bibliotek odpowiadajacych za rodzaj wprowadzanych danych 
from wtforms import StringField, PasswordField, SubmitField  # Fields for user inputs
# Klasa length sluzy do wyznaczania dlugosci, EqualTo sprawdza czy wartosci sa takie same, Email sprawdza czy ktos podal wlasciwy email
# DataRequired sprawia, ze pole musi byc wypelnione
from wtforms.validators import Length, EqualTo , Email, DataRequired, ValidationError
from market.models import User
# jesli uzywamy wiecej warunkow, nalezy wpisac je w liscie ([warunek,warunek])


class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[Length(min=3, max=20), DataRequired()])
    email = StringField(label="Email", validators=[Email(),DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label="Create Account")


    def validate_username(self,username_to_check):
            #Zapisujemy w zmiennej usera, ktory jest taki sam jak username to check
        user = User.query.filter_by(username = username_to_check.data).first()
        if user: # jesli user istnieje to oznacza, ze ktos juz ma taka nazwe
            # bo zostanie zwrocona nam wartosc
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