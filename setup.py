# http://flask.pocoo.org/docs/0.12/patterns/distribute/
from setuptools import find_packages
from distutils.core import setup

setup(
    name='nbi-projects-site',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask_wtf',
        'WTForms'
    ]
)
