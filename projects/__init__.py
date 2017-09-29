import os, jinja2
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from nbi_base import app

# Load multiple shared_templates paths
all_temp = [os.path.abspath("projects/templates"), app.root_path + "/templates"]
custom_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader(all_temp)])
app.jinja_loader = custom_loader

csrf = CSRFProtect(app)
app.secret_key = os.urandom(24)
Bootstrap(app)

print("all temp: " + str(all_temp))
print("Instance path: " + app.instance_path)
print("Root path: " + app.root_path)
print("Static urlpath: " + app.static_url_path)
print("static folder: " + app.static_folder)
print("obs path: " + os.path.abspath(""))


## Setup projects config statics
import projects.conf
import projects.nav
import projects.views