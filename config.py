import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask configuration
SECRET_KEY = 'ffcs-timetable-builder-secret-key-2024'
DEBUG = True

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'timetable.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
