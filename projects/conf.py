import os
from projects import app
from projects.models import User
from bcrypt import gensalt


# Required folders
folders = {}
folders['DATA_FOLDER'] = app.config['DATA_FOLDER'] = os.path.abspath('projects/persistence/data')
folders['UPLOAD_FOLDER'] = app.config['UPLOAD_FOLDER'] = os.path.abspath('projects/persistence/images')

## Create required folders for the application if they don't exist
for key, folder in folders.items():
    try:
        os.makedirs(folder)
        print("Created: " + folder)
    except FileExistsError:
        pass

## Default db target
app.config['DB'] = app.config['DATA_FOLDER'] + "/projects_dev"

# Password Salt
exists = os.path.isfile(os.path.abspath("salt.file"))
if exists:
    string = open(os.path.abspath("salt.file"), 'r').read()
    salt = string.encode()
else:
    salt = gensalt()
    open(os.path.abspath("salt.file"), 'w').write(str(salt, 'utf-8'))

app.config['SECURITY_PASSWORD_SALT'] = salt

# Projects static folder
app.config['PROJECTS_STATIC_FOLDER'] = os.path.abspath("projects/static")

# Application admins
app.config['ADMINS'] = ['rasmus.munk@nbi.ku.dk']

# Email application server
app.config['MAIL_SERVER'] = 'smtp.live.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']

# TODO -> remove before commit
# Debug
user = User.get_with_first('email', app.config['ADMINS'][0])
if user is not None:
    User.remove(user._id)
