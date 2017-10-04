# http://flask.pocoo.org/snippets/62/
from projects import app
from urllib.parse import urlparse, urljoin
from flask import request, url_for
from projects.models import User
from projects import login_manager
from itsdangerous import URLSafeTimedSerializer, BadSignature


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


## LoginManager
@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


## A token is valid for a day
def confirm_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except BadSignature:
        return False
    return email
