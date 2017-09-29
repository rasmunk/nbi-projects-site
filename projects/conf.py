import os
from projects import app

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

# common static folder path
app.config['STATIC_FOLDER'] = os.path.abspath("nbi_base/static")

## Default db target
app.config['DB'] = app.config['DATA_FOLDER'] + "/projects_dev"

## Projects static folder
app.config['PROJECTS_STATIC_FOLDER'] = os.path.abspath("projects/static")