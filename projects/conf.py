import os
from projects import app
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

# Default db target
app.config['DB'] = app.config['DATA_FOLDER'] + "/projects_dev"

# Password Salt
# Store in persistence directory
exists = os.path.isfile(app.config['DATA_FOLDER'] + "/salt.file")
if exists:
    string = open(app.config['DATA_FOLDER'] + "/salt.file", 'r').read()
    salt = str(string)
else:
    salt = str(gensalt(), 'utf-8')
    open(app.config['DATA_FOLDER'] + "/salt.file", 'w').write(salt)

app.config['SECURITY_PASSWORD_SALT'] = salt

# Projects static folder
app.config['PROJECTS_STATIC_FOLDER'] = os.path.abspath("projects/static")

# Application ADMINS_EMAIL
app.config['ADMINS_EMAIL'] = os.environ['ADMINS_EMAIL'].split(',')

# Email application server
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
app.config['MAIL_USE_TLS'] = bool(os.environ['MAIL_USE_TLS'])
app.config['MAIL_USE_SSL'] = False if os.environ['MAIL_USE_SSL'] == 'False' else True
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']

