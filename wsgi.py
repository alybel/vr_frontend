__author__ = 'matyas'
import os
import app as Application
from flask.ext.script import Manager, Shell

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    Application.run()