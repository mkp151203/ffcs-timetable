from flask import Blueprint, jsonify, request
from models import db, Course, Slot, Faculty, Registration

courses_bp = Blueprint('courses', __name__)


@courses_bp.route('/search')
def search_courses():
    """Search courses by code or name."""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'courses': []})
    
    courses = Course.query.filter(
        db.or_(
            Course.code.ilike(f'%{query}%'),
            Course.name.ilike(f'%{query}%')
        )
    ).limit(20).all()
    
    return jsonify({
        'courses': [course.to_dict() for course in courses]
    })


@courses_bp.route('/<int:course_id>')
def get_course(course_id):
    """Get course details by ID."""
    course = Course.query.get_or_404(course_id)
    return jsonify(course.to_dict())


@courses_bp.route('/<int:course_id>/slots')
def get_course_slots(course_id):
    """Get all available slots for a course."""
    course = Course.query.get_or_404(course_id)
    slots = Slot.query.filter_by(course_id=course_id).all()
    
    return jsonify({
        'course': course.to_dict(),
        'slots': [slot.to_dict() for slot in slots]
    })


@courses_bp.route('/all')
def get_all_courses():
    """Get all courses."""
    courses = Course.query.order_by(Course.code).all()
    return jsonify({
        'courses': [course.to_dict() for course in courses]
    })


@courses_bp.route('/manual', methods=['POST'])
def add_course_manually():
    """Add a course manually with slot and auto-register."""
    data = request.get_json()
    
    # Validate required fields
    required = ['course_code', 'course_name', 'slot_code']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        # Find or create course
        course = Course.query.filter_by(code=data['course_code'].upper()).first()
        if not course:
            course = Course(
                code=data['course_code'].upper(),
                name=data['course_name'],
                l=0,
                t=0,
                p=0,
                j=0,
                c=int(data.get('credits', 0)),
                course_type='N/A',
                category='N/A'
            )
            db.session.add(course)
            db.session.flush()
        
        # Find or create faculty
        faculty_name = data.get('faculty', 'N/A').strip() or 'N/A'
        faculty = Faculty.query.filter_by(name=faculty_name).first()
        if not faculty:
            faculty = Faculty(name=faculty_name)
            db.session.add(faculty)
            db.session.flush()
        
        # Create slot
        venue = data.get('venue', 'N/A').strip().upper() or 'N/A'
        slot = Slot(
            slot_code=data['slot_code'].upper(),
            course_id=course.id,
            faculty_id=faculty.id,
            venue=venue,
            available_seats=70,
            total_seats=70
        )
        db.session.add(slot)
        db.session.flush()
        
        # Auto-register
        registration = Registration(slot_id=slot.id)
        db.session.add(registration)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f"Course {course.code} added and registered successfully!",
            'course': course.to_dict(),
            'slot': slot.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
