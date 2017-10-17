# Load enviroment variables
exec(open("./projects-envvars.py").read())
from projects import app
from projects.models import User
from bcrypt import hashpw
import datetime

if __name__ == '__main__':
    # Implement test user
    user = User.get_with_first('email', 'test@nbi.ku.dk')
    if user is None:
        user = User(email='test@nbi.ku.dk', password=hashpw(bytes("test", 'utf-8'), bytes(app.config['SECURITY_PASSWORD_SALT'], 'utf-8')),
                    projects=[], is_active=True, is_authenticated=True, is_anonymous=False,
                    confirmed_on=datetime.datetime.now())
        user.save()
    app.run(debug=True)

