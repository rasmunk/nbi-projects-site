import os, jinja2
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from nbi_base import app

# Load multiple shared_templates paths
all_temp = [os.path.abspath("projects/templates"), app.root_path + "/templates"]
custom_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader(all_temp)])
app.jinja_loader = custom_loader

csrf = CSRFProtect(app)
app.secret_key = os.urandom(24)
Bootstrap(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import projects.conf
# Connect mail
mail = Mail(app)

## Setup projects config statics

import projects.nav
import projects.views