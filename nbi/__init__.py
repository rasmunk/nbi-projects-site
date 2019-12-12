import os
from flask import Flask, Blueprint
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_nav import Nav
from projects import base_blueprint
from projects import projects_blueprint
from projects.forms import ProjectFormManager
from nbi.conf import config
from nbi.forms import NBIProjectForm

app = Flask(__name__)

nbi_blueprint = Blueprint('nbi', __name__,
                          static_folder='static',
                          static_url_path='/nbi/static',
                          template_folder='templates')

app.register_blueprint(base_blueprint)
app.register_blueprint(projects_blueprint)
app.register_blueprint(nbi_blueprint)

csrf = CSRFProtect(app)
app.secret_key = os.urandom(24)
Bootstrap(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Connect mail
mail = Mail(app)
# project_manager = ProjectFormManager()
# project_manager.register_form_class(config.get('PROJECTS', 'form_class'),
#                                     config.get('PROJECTS', 'form_module',
#                                                **{'fallback': None}))
# Setup navbar
nav = Nav()
nav.init_app(app)
import nbi.nav

# Onetime authentication reset token salt
app.config['ONETIME_TOKEN_SALT'] = os.urandom(24)

# # If debug option
# if app.debug:
#     # Implement test user
#     user = User.get_with_first('email', 'test@nbi.ku.dk')
#     if user is None:
#         user = User(email='test@nbi.ku.dk',
#                     password=hashpw(bytes("test", 'utf-8'),
#                                     gensalt()),
#                     projects=[], is_active=True,
#                     is_authenticated=True, is_anonymous=False,
#                     confirmed_on=datetime.datetime.now())
#         user.save()
