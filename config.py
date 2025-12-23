import os
import dotenv
dotenv.load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
DEBUG = True

# Database configuration
# Database configuration
if os.environ.get('VERCEL'):
    # Vercel filesystem is read-only, use ephemeral /tmp
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/timetable.db'
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'timetable.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'placeholder-client-id')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'placeholder-client-secret')
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
