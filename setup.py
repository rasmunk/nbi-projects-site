# http://flask.pocoo.org/docs/0.12/patterns/distribute/
from setuptools import find_packages
from distutils.core import setup

setup(
    name='projects',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'flask-bootstrap',
        'flask-nav',
        'flask-wtf',
        'WTForms',
        'requests',
        'wtforms-components',
        'flask_login',
        'flask_mail',
        'bcrypt',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
