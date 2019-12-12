import os
from projects.conf import config

config.read(os.path.abspath(
    os.path.join('nbi-projects-site', 'res', 'config.ini')))
