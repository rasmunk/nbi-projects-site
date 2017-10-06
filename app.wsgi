#!/usr/bin/python3
import os
# Load environment variables
exec(open(os.path.join(os.environ['NBI_PROJECTS_DIR'], 'projects-envvars.py')).read())
from projects import app as application