# Setup required environment variables
exec(open("./projects-envvars.py").read())
from projects import app

if __name__ == '__main__':

    app.run(debug=True)
