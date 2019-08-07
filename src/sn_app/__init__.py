
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_security.forms import RegisterForm
from flask_security import Security, SQLAlchemySessionUserDatastore, UserMixin, RoleMixin, login_required
from sn_app.database import db_session, init_db
from sn_app.models import User, Role
from flask_mail import Mail

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/create_account'
# app.config['MAIL_SERVER'] = 'smtp.example.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'username'
# app.config['MAIL_PASSWORD'] = 'password'

db = SQLAlchemy(app)
Bootstrap(app)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore, register_form="security/register_user.html")

mail = Mail(app)

@app.before_first_request
def create_user():
    init_db()
    if not user_datastore.find_user(email='test@test.com'):
        user_datastore.create_user(username='test', email='test@test.com', password='password')
    db_session.commit()

from sn_app import views

