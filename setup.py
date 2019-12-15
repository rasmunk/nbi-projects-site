# http://flask.pocoo.org/docs/0.12/patterns/distribute/
from setuptools import find_packages
from distutils.core import setup

setup(
    name='nbi-projects-site',
    version='0.0.1',
    url='https://github.com/rasmunk/nbi-projects-site',
    author='Rasmus Munk',
    author_email='rasmus.munk@nbi.ku.dk',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords=['Website', 'Flask', 'MetaData'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask_wtf',
        'WTForms'
    ]
)
