
from flask import render_template
from sn_app import app
from flask_security import Security, SQLAlchemySessionUserDatastore, UserMixin, RoleMixin, login_required

@app.route('/')
def index():
    return render_template('index.html')

