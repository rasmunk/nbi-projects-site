# Load enviroment variables
exec(open("./projects-envvars.py").read())
import datetime
from projects import app
from projects.models import User
from bcrypt import hashpw, gensalt

if __name__ == '__main__':
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
    app.run(host='0.0.0.0', port=80, debug=True)
