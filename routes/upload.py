"""Routes for HTML file upload and parsing."""

from flask import Blueprint, request, jsonify, session
from models import db, Course, Faculty, Slot
from utils.html_parser import parse_vtop_html

upload_bp = Blueprint('upload', __name__)
@upload_bp.route('/parse', methods=['POST'])
def parse_html_file():
    """
    Parse uploaded HTML file and extract course/slot information.
    Returns parsed data without saving to database.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith(('.html', '.htm', '.mhtml')):
        return jsonify({'error': 'File must be HTML or MHTML'}), 400
    
    try:
        html_content = file.read().decode('utf-8')
        parsed = parse_vtop_html(html_content)
        
        if not parsed['course']:
            return jsonify({'error': 'Could not parse course information from HTML'}), 400
        
        return jsonify({
            'success': True,
            'course': parsed['course'],
            'slots': parsed['slots'],
            'slot_count': len(parsed['slots'])
        })
        
    except Exception as e:
        return jsonify({'error': f'Error parsing file: {str(e)}'}), 500

@upload_bp.route('/import', methods=['POST'])
def import_html_file():
    """
    Parse uploaded HTML files and save data to database.
    Accepts multiple files key 'files[]'.
    """
    files = request.files.getlist('files[]')
    
    if not files:
        # Fallback for single file 'file' logic if needed, or just error
        if 'file' in request.files:
            files = [request.files['file']]
        else:
            return jsonify({'error': 'No files provided'}), 400
    
    # Determine owner
    user_id = session.get('user_id')
    guest_id = session.get('guest_id')
    
    if not user_id and not guest_id:
        return jsonify({'error': 'No active session'}), 401

    results = []
    success_count = 0
    
    for file in files:
        if file.filename == '':
            continue
            
        if not file.filename.lower().endswith(('.html', '.htm', '.mhtml')):
            results.append({
                'filename': file.filename,
                'status': 'error',
                'message': 'Invalid file type'
            })
            continue

        try:
            # Process single file
            result = _process_single_file_import(file, user_id, guest_id)
            results.append(result)
            if result['status'] == 'success':
                success_count += 1
                
        except Exception as e:
            # DB Rollback handled inside helper or here if transaction spans whole loop?
            # We want partial success, so _process_single_file_import should handle its own transaction lifecycle 
            # OR we handle it here. 
            # If we want to isolate errors, we should commit/rollback per file.
            db.session.rollback() 
            results.append({
                'filename': file.filename,
                'status': 'error',
                'message': str(e)
            })

    return jsonify({
        'success': True,
        'summary': f'Processed {len(files)} files. {success_count} succeeded.',
        'results': results,
        'success_count': success_count
    })

def _process_single_file_import(file, user_id, guest_id):
    """Helper to process a single file import within the batch."""
    try:
        html_content = file.read().decode('utf-8')
        parsed = parse_vtop_html(html_content)
        
        if not parsed['course']:
            return {'filename': file.filename, 'status': 'error', 'message': 'Could not parse course info'}
        
        course_data = parsed['course']
        
        # Check if course already exists FOR THIS USER
        query = Course.query.filter_by(code=course_data['code'])
        if user_id:
            query = query.filter_by(user_id=user_id)
        else:
            query = query.filter_by(guest_id=guest_id)
            
        course = query.first()
        
        # Start Transaction for this file
        if not course:
            course = Course(
                code=course_data['code'],
                name=course_data['name'],
                l=course_data['l'],
                t=course_data['t'],
                p=course_data['p'],
                j=course_data['j'],
                c=course_data['c'],
                course_type=course_data['course_type'],
                category=course_data['category'],
                user_id=user_id,
                guest_id=guest_id
            )
            db.session.add(course)
            db.session.flush()
        
        # --- Batch Process Faculties ---
        faculty_names = set(s['faculty'] for s in parsed['slots'] if s['faculty'])
        
        # Note: In a batch loop, re-querying faculties every time is safe.
        existing_faculties = Faculty.query.filter(Faculty.name.in_(faculty_names)).all()
        faculty_map = {f.name: f for f in existing_faculties}
        
        missing_names = faculty_names - set(faculty_map.keys())
        if missing_names:
            new_facs = []
            for name in missing_names:
                f = Faculty(name=name)
                new_facs.append(f)
            
            db.session.add_all(new_facs)
            db.session.flush()
            
            for f in new_facs:
                faculty_map[f.name] = f

        # --- Batch Process Slots ---
        existing_slots = Slot.query.filter_by(course_id=course.id).all()
        existing_slot_signatures = {(s.slot_code, s.venue) for s in existing_slots}
        
        slots_to_add = []
        for slot_data in parsed['slots']:
            signature = (slot_data['slot_code'], slot_data['venue'])
            
            if signature not in existing_slot_signatures:
                faculty = faculty_map.get(slot_data['faculty'])
                new_slot = Slot(
                    slot_code=slot_data['slot_code'],
                    course_id=course.id,
                    faculty_id=faculty.id if faculty else None,
                    venue=slot_data['venue'],
                    available_seats=slot_data['available_seats'],
                    total_seats=70,
                    class_nbr=slot_data.get('class_nbr')
                )
                slots_to_add.append(new_slot)
                existing_slot_signatures.add(signature)
        
        if slots_to_add:
            db.session.add_all(slots_to_add)
            slots_added = len(slots_to_add)
        else:
            slots_added = 0
        
        # Commit per file to avoid huge transactions and ensure partial batch success
        db.session.commit()
        
        return {
            'filename': file.filename,
            'status': 'success',
            'course_code': course_data['code'],
            'slots_added': slots_added
        }
        
    except Exception as e:
        db.session.rollback()
        raise e # Re-raise to be caught by the loop handler
