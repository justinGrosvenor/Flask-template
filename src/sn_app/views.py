
from flask import render_template, url_for, flash, redirect
from sn_app import app, db, bcrypt
from flask_security import Security, SQLAlchemySessionUserDatastore, UserMixin, RoleMixin, login_required
from flask_security.forms import RegisterForm
from sn_app.models import User, Role


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('account created', 'success')
        return redirect('/login')
    return render_template('/security/register_user.html')

@app.route('/login')
def login():
	return redirect('/')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')