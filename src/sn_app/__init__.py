
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_security.forms import RegisterForm
from flask_security import Security, SQLAlchemySessionUserDatastore, UserMixin, RoleMixin, login_required
from sn_app.database import db_session, init_db
from sn_app.models import User, Role
# from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt

app = Flask(__name__)



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = "2987djakfh982rhfs9"
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
# app.config['MAIL_SERVER'] = 'localhost'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = 'username'
# app.config['MAIL_PASSWORD'] = 'password'
# app.config['SECURITY_EMAIL_SENDER'] = 'example@gmail.com'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
# mail = Mail(app)
Bootstrap(app)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


admin = Admin(app, name='admin')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))

@app.before_first_request
def create_user():
    init_db()
    if not user_datastore.find_user(email='test@test.com'):
        user_datastore.create_user(username='test', email='test@test.com', password='password')
    db_session.commit()

from sn_app import views

