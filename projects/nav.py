from projects import app
from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()


@nav.navigation()
def nav_bar():
    return Navbar(
        View('eScience Projects', '.projects'),
        View('Projects', '.projects'),
        View('Create Project', '.create'),
    )
nav.init_app(app)
