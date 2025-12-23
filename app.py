from flask import Flask
from models import db
from routes import main_bp, courses_bp, registration_bp, upload_bp

app = Flask(__name__)
app.config.from_object('config')

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(courses_bp, url_prefix='/api/courses')
app.register_blueprint(registration_bp, url_prefix='/api/registration')
app.register_blueprint(upload_bp, url_prefix='/api/upload')

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
