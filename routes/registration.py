from flask import Blueprint, jsonify, request
from models import db, Registration, Slot
from models.slot import get_slot_timing

registration_bp = Blueprint('registration', __name__)


@registration_bp.route('/', methods=['GET'])
def get_registrations():
    """Get all registered courses."""
    registrations = Registration.query.all()
    return jsonify({
        'registrations': [reg.to_dict() for reg in registrations],
        'count': len(registrations),
        'total_credits': sum(
            reg.slot.course.c for reg in registrations 
            if reg.slot and reg.slot.course
        )
    })


@registration_bp.route('/', methods=['POST'])
def register_course():
    """Register a new course slot."""
    data = request.get_json()
    slot_id = data.get('slot_id')
    
    if not slot_id:
        return jsonify({'error': 'slot_id is required'}), 400
    
    # Check if slot exists
    slot = Slot.query.get(slot_id)
    if not slot:
        return jsonify({'error': 'Slot not found'}), 404
    
    # Check if already registered for this course
    existing = Registration.query.join(Slot).filter(
        Slot.course_id == slot.course_id
    ).first()
    if existing:
        return jsonify({'error': 'Already registered for this course'}), 400
    
    # Check for clashes
    clash_result = check_slot_clashes(slot)
    if clash_result['has_clash']:
        return jsonify({
            'error': 'Slot clash detected',
            'clashing_slots': clash_result['clashing_slots']
        }), 400
    
    # Create registration
    registration = Registration(slot_id=slot_id)
    db.session.add(registration)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'registration': registration.to_dict()
    }), 201


@registration_bp.route('/<int:reg_id>', methods=['DELETE'])
def delete_registration(reg_id):
    """Delete a registration."""
    registration = Registration.query.get_or_404(reg_id)
    db.session.delete(registration)
    db.session.commit()
    
    return jsonify({'success': True})


@registration_bp.route('/check-clash', methods=['POST'])
def check_clash():
    """Check if a slot would clash with existing registrations."""
    data = request.get_json()
    slot_id = data.get('slot_id')
    
    if not slot_id:
        return jsonify({'error': 'slot_id is required'}), 400
    
    slot = Slot.query.get(slot_id)
    if not slot:
        return jsonify({'error': 'Slot not found'}), 404
    
    result = check_slot_clashes(slot)
    return jsonify(result)


@registration_bp.route('/credits', methods=['GET'])
def get_credits():
    """Get current credit summary."""
    registrations = Registration.query.all()
    total_credits = sum(
        reg.slot.course.c for reg in registrations 
        if reg.slot and reg.slot.course
    )
    
    return jsonify({
        'total_credits': total_credits,
        'max_credits': 27,
        'min_credits': 16,
        'course_count': len(registrations)
    })


def check_slot_clashes(new_slot):
    """Check if a new slot clashes with existing registrations."""
    # Get all individual slots from the new slot
    new_individual_slots = new_slot.get_individual_slots()
    
    # Get all registered slots
    registrations = Registration.query.all()
    
    clashing_slots = []
    
    for reg in registrations:
        if reg.slot:
            registered_individual_slots = reg.slot.get_individual_slots()
            
            # Check for overlap
            for new_s in new_individual_slots:
                new_timing = get_slot_timing(new_s)
                if not new_timing:
                    continue
                    
                for reg_s in registered_individual_slots:
                    reg_timing = get_slot_timing(reg_s)
                    if not reg_timing:
                        continue
                    
                    # Clash if same day and same period
                    if (new_timing['day'] == reg_timing['day'] and 
                        new_timing['period'] == reg_timing['period']):
                        clashing_slots.append({
                            'slot_code': reg.slot.slot_code,
                            'course_code': reg.slot.course.code if reg.slot.course else '',
                            'course_name': reg.slot.course.name if reg.slot.course else ''
                        })
                        break
    
    return {
        'has_clash': len(clashing_slots) > 0,
        'clashing_slots': clashing_slots
    }
