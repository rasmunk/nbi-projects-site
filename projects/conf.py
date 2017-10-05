import os
from projects import app
from getpass import getpass
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
    salt = str(string)
else:
    salt = gensalt()
    open(os.path.abspath("salt.file"), 'w').write(str(salt, 'utf-8'))

app.config['SECURITY_PASSWORD_SALT'] = salt

# Projects static folder
app.config['PROJECTS_STATIC_FOLDER'] = os.path.abspath("projects/static")

# Application ADMINS_EMAIL
app.config['ADMINS_EMAIL'] = os.environ['ADMINS_EMAIL']

# Email application server
# TODO -> switch from live to nbi email server
app.config['MAIL_SERVER'] = 'smtp.live.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
if 'MAIL_PASSWORD' not in app.config:
    app.config['MAIL_PASSWORD'] = getpass('Provide the mail service users password')
