from flask import Flask
from models import db
from routes import main_bp, courses_bp, registration_bp, upload_bp, auth_bp
from routes.auth import init_oauth

app = Flask(__name__)
app.config.from_object('config')

# Initialize database
db.init_app(app)

# Initialize OAuth
init_oauth(app)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(courses_bp, url_prefix='/api/courses')
app.register_blueprint(registration_bp, url_prefix='/api/registration')
app.register_blueprint(upload_bp, url_prefix='/api/upload')

# Create tables
with app.app_context():
    db.create_all()

@app.after_request
def add_header(response):
    """Add headers to prevent caching."""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Background Cleanup Task
import threading
import time
from datetime import datetime, timedelta
from models import Course

def cleanup_orphaned_data():
    """Delete guest data older than 24 hours."""
    while True:
        try:
            with app.app_context():
                # Define cutoff time (24 hours ago)
                cutoff = datetime.utcnow() - timedelta(hours=24)
                
                # Find old guest courses
                old_courses = Course.query.filter(
                    Course.guest_id.isnot(None), 
                    Course.created_at < cutoff
                ).all()
                
                if old_courses:
                    print(f"[{datetime.now()}] Cleanup: Deleting {len(old_courses)} orphaned guest courses...")
                    for course in old_courses:
                        db.session.delete(course)
                    
                    db.session.commit()
                    print(f"[{datetime.now()}] Cleanup complete.")
                
        except Exception as e:
            print(f"Cleanup error: {e}")
            
        # Run every hour (3600 seconds)
        time.sleep(3600)

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_orphaned_data, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
