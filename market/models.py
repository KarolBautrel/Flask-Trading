from market import db, bcrypt, login_manager, mail
from flask_login import UserMixin
from flask_mail import Message

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30),nullable=False, unique=True)
    email_address = db.Column(db.String(length=50),nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60),nullable=False)
    budget = db.Column(db.Integer(),nullable=False,default=1000)
    items = db.relationship('Item', backref ='owned_user', lazy = True) #backer to back reference to User model


    
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')




    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


    def can_purchase(self, item_object):
        return self.budget >= item_object.price



    def registration_mail(self):
        msg = Message("Account creation", sender = 'testbautrel111@gmail.com', recipients = [self.email_address])
        msg.body = (f'Your account has been created. Your name is {self.username}, have a good time on our store')
        mail.send(msg)  




    def change_password(self, input_password):
        self.password_hash = bcrypt.generate_password_hash(input_password).decode('utf-8')
        db.session.commit()
        
    def change_email(self, input_email):
        self.email_address = input_email
        db.session.commit()






class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    picture = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

        
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()