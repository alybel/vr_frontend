__author__ = 'matyas'
import os, sys
from app import *
sys.path.append('/home/matyas/vr_frontend/')

application = create_app("development")

#sys.path.append('/home/matyas/vr_frontend/')
#app = create_app(os.getenv('FLASK_CONFIG') or 'default')

#if __name__ == '__main__':
#    app.run()
