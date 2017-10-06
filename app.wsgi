#!/usr/bin/python3
import os
# Load enviroment variables
exec(open("./projects-envvars.py").read())
# Used by the apache wsgi module
from projects import app as application