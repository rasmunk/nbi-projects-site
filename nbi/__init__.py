import os
import datetime
from bcrypt import hashpw, gensalt
from flask import Flask, Blueprint
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_nav import Nav
from projects import base_blueprint, projects_blueprint
from projects.models import User
from projects.helpers import load_user
from projects.nav import nav_bar
from nbi.forms import NBIProjectForm

app = Flask(__name__)
nbi_blueprint = Blueprint('nbi', __name__,
                          static_folder='static',
                          static_url_path='/nbi/static',
                          template_folder='templates')
app.register_blueprint(base_blueprint)

csrf = CSRFProtect(app)
app.secret_key = os.urandom(24)
Bootstrap(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def nbi_load_user(user_id):
    return load_user(user_id)


# Connect mail
mail = Mail(app)

# Setup navbar
nav = Nav()
nav.init_app(app)
nav.register_element('nav_bar', nav_bar)
import nbi.views
app.register_blueprint(nbi_blueprint)
# Turn of the default endpoint
app.register_blueprint(projects_blueprint)

# Onetime authentication reset token salt
app.config['ONETIME_TOKEN_SALT'] = os.urandom(24)

# If debug option
if app.debug:
    # Implement test user
    user = User.get_with_first('email', 'test@nbi.ku.dk')
    if user is None:
        user = User(email='test@nbi.ku.dk',
                    password=hashpw(bytes("test", 'utf-8'),
                                    gensalt()),
                    projects=[], is_active=True,
                    is_authenticated=True, is_anonymous=False,
                    confirmed_on=datetime.datetime.now())
        user.save()
