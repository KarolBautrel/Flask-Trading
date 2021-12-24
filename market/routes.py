from market import app, db, oauth
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellingItemForm, ChangePasswordForm, ChangeEmailForm

google = oauth.register(
    name='google',
    client_id="378796742278-5r3jjcc9m0hdvh8864l4on1lt49kcgc1.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market',methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name = purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'{p_item_object.name} bought successfully', category='success')
            else:
                flash('Not enough money', category= "danger")
        return redirect(url_for('owned_page'))
       
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None) # wyswietlenie wszystkich obiektow w naszej bazie danych
        
        return render_template('market.html', items=items, purchase_form=purchase_form)

   
    


@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                              email_address = form.email.data,
                                password = form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error with creating an user: {err_msg}", category = 'danger')

    return render_template('register.html', form=form)
@app.route('/login/gmail')
def login_gmail():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)




@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    
    session['profile'] = user_info
    print(user_info)
    google_user = User.query.filter_by(username=user_info['name']).first()
    if not google_user:
        new_google_user = User(username = user_info['name'], 
                                email_address=user_info['email'],
                                password =user_info['id'] )
        db.session.add(new_google_user)
        db.session.commit()
        login_user(new_google_user)
        flash(f'You are logged by your google account.',category = "success")
        return redirect('/market')
    else: 
        login_user(google_user)
        flash(f'You are logged by your google account.' , category = "success")
        session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
        return redirect('/market')







@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Succes! You are logged in as {attempted_user.username}', category="success")
            return(redirect(url_for('market_page')))
        else:
            flash("Username or password are not match", category='danger')
    return render_template('login.html' ,form=form)




@app.route('/owned', methods=['GET','POST'])
@login_required
def owned_page():
    sold_form = SellingItemForm()
    if request.method == 'POST':
         selling_item = request.form.get('sold_item')
         s_item_object = Item.query.filter_by(name = selling_item).first()
         if s_item_object:
            s_item_object.sell(current_user)
            flash(f'{s_item_object.name} has been sold', category = "success")
            return redirect(url_for('market_page')) # powrot do marketu po kupnie

    if request.method == 'GET':
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('owned.html' ,owned_items=owned_items, sold_form=sold_form)


@app.route('/panel',methods=['GET', 'POST'])
@login_required
def panel_page():
    
    return render_template('panel.html')


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password_page():
    form = ChangePasswordForm()
    if form.validate_on_submit():
            if current_user.check_password_correction(attempted_password=form.old_password.data):
                current_user.change_password(form.new_password.data)
                flash(f'Password has been changed', category= "success")
                return redirect(url_for('panel_page'))
            else:
                flash('Wrong password')
    return render_template('change_password.html', form=form)



@app.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_page():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.check_password_correction(attempted_password=form.password.data):
            current_user.change_email(form.email.data)
            flash(f'Email has been changed', category= "success")
            return redirect(url_for('panel_page'))
        else:
            flash('Wrong password')
        
    return render_template('change_email.html', form=form)



@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You are logged out', category='info')
    return redirect(url_for('home_page'))