import os
from projects import app

# Required folders
folders = {}
folders['DATA_FOLDER'] = app.config['DATA_FOLDER'] = os.path\
    .abspath('projects/persistence/data')
folders['UPLOAD_FOLDER'] = app.config['UPLOAD_FOLDER'] = os.path\
    .abspath('projects/persistence/images')

# Create required folders for the application if they don't exist
for key, folder in folders.items():
    try:
        os.makedirs(folder)
        print("Created: " + folder)
    except FileExistsError:
        pass

# Db lockfile
app.config['DB_LOCK'] = os.path.join(app.config['DATA_FOLDER'],
                                     'projects_db_lock')

# Default db target
app.config['DB'] = os.path.join(app.config['DATA_FOLDER'], "projects_dev")

# Onetime authentication reset token salt
app.config['ONETIME_TOKEN_SALT'] = os.urandom(24)

# Projects static folder
app.config['PROJECTS_STATIC_FOLDER'] = os.path.abspath("projects/static")

# Application ADMINS_EMAIL
app.config['ADMINS_EMAIL'] = os.environ['ADMINS_EMAIL'].split(',')

# Email application server
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
app.config['MAIL_USE_TLS'] = bool(os.environ['MAIL_USE_TLS'])
app.config['MAIL_USE_SSL'] = False if os.environ['MAIL_USE_SSL'] == 'False'\
                                   else True
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']

