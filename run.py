# Load enviroment variables
import os
if os.environ['ENV_DIR']:
    exec(open(os.path.join(os.environ['ENV_DIR'],
                           'projects-envvars.py')).read())
else:
    exec(open("./projects-envvars.py").read())

import datetime
import argparse
from projects import app
from projects.models import User
from bcrypt import hashpw, gensalt

# Handling arguments
parser = argparse.ArgumentParser(description='Start the projects website')
parser.add_argument('--debug', dest='debug', action='store_true',
                    default=False,
                    help='Whether the application should run in debug mode')
parser.add_argument('--port', dest='port', type=int, default=80,
                    help='The port the webserver should listen on')
args = parser.parse_args()

if __name__ == '__main__':
    if args.debug:
        # Implement test user
        user = User.get_with_first('email', 'test@nbi.ku.dk')
        if user is None:
            user = User(email='test@nbi.ku.dk',
                        password=hashpw(bytes("test", 'utf-8'),
                                        gensalt()),
                        projects=[], is_active=True,
                        is_authenticated=True, is_anonymous=False,
                        confirmed_on=datetime.datetime.now())
            user.save()
    app.run(host='0.0.0.0', port=args.port, debug=args.debug)
