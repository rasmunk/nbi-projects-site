# This file contains the environment variable setup that is required before the application is run
import os

# Mail server setup for MAIL_USERNAME
# Default to outlook email
os.environ['MAIL_SERVER'] = 'smtp.live.com'
os.environ['MAIL_PORT'] = '25'
os.environ['MAIL_USE_TLS'] = 'True'
os.environ['MAIL_USE_SSL'] = 'False'

# Used to send authentication requests
os.environ['MAIL_USERNAME'] = 'email'
os.environ['MAIL_PASSWORD'] = 'password'

# Used to approve authentication requests received by MAIL_USERNAME
# comma seperate if more should be included
os.environ['ADMINS_EMAIL'] = 'authentication_grant_email'
