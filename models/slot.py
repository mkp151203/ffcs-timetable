from .database import db


class Slot(db.Model):
    """Slot model representing a course slot with timing, faculty, and venue."""
    
    __tablename__ = 'slots'
    
    id = db.Column(db.Integer, primary_key=True)
    slot_code = db.Column(db.String(50), nullable=False)  # e.g., "A11+A12", "B21+E14"
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    venue = db.Column(db.String(50), nullable=False)  # e.g., "CR-011", "AB02-330"
    available_seats = db.Column(db.Integer, default=0)
    total_seats = db.Column(db.Integer, default=70)
    class_nbr = db.Column(db.String(50), nullable=True)  # Unique class identifier
    
    def __repr__(self):
        return f'<Slot {self.slot_code} - {self.venue}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'slot_code': self.slot_code,
            'course_id': self.course_id,
            'course': self.course.to_dict() if self.course else None,
            'faculty_id': self.faculty_id,
            'faculty_name': self.faculty.name if self.faculty else None,
            'venue': self.venue,
            'available_seats': self.available_seats,
            'total_seats': self.total_seats,
            'class_nbr': self.class_nbr,
            'is_full': False  # No seat limit - always allow registration
        }
    
    def get_individual_slots(self):
        """Parse slot_code like 'A11+A12' into list ['A11', 'A12']."""
        return self.slot_code.replace('/', '+').split('+')


# Slot timing reference - maps slot codes to day and period
SLOT_TIMINGS = {
    # Period 1: 08:30 - 10:00
    'A11': {'day': 'MON', 'period': 1, 'start': '08:30', 'end': '10:00'},
    'B11': {'day': 'TUE', 'period': 1, 'start': '08:30', 'end': '10:00'},
    'C11': {'day': 'WED', 'period': 1, 'start': '08:30', 'end': '10:00'},
    'D11': {'day': 'THU', 'period': 1, 'start': '08:30', 'end': '10:00'},
    'E11': {'day': 'FRI', 'period': 1, 'start': '08:30', 'end': '10:00'},
    'F11': {'day': 'SAT', 'period': 1, 'start': '08:30', 'end': '10:00'},
    
    # Period 2: 10:05 - 11:35
    'A12': {'day': 'MON', 'period': 2, 'start': '10:05', 'end': '11:35'},
    'B12': {'day': 'TUE', 'period': 2, 'start': '10:05', 'end': '11:35'},
    'C12': {'day': 'WED', 'period': 2, 'start': '10:05', 'end': '11:35'},
    'D12': {'day': 'THU', 'period': 2, 'start': '10:05', 'end': '11:35'},
    'E12': {'day': 'FRI', 'period': 2, 'start': '10:05', 'end': '11:35'},
    'F12': {'day': 'SAT', 'period': 2, 'start': '10:05', 'end': '11:35'},
    
    # Period 3: 11:40 - 13:10
    'A13': {'day': 'MON', 'period': 3, 'start': '11:40', 'end': '13:10'},
    'B13': {'day': 'TUE', 'period': 3, 'start': '11:40', 'end': '13:10'},
    'C13': {'day': 'WED', 'period': 3, 'start': '11:40', 'end': '13:10'},
    'D13': {'day': 'THU', 'period': 3, 'start': '11:40', 'end': '13:10'},
    'E13': {'day': 'FRI', 'period': 3, 'start': '11:40', 'end': '13:10'},
    'F13': {'day': 'SAT', 'period': 3, 'start': '11:40', 'end': '13:10'},
    
    # Period 4 (After Lunch): 13:15 - 14:45
    'A14': {'day': 'MON', 'period': 4, 'start': '13:15', 'end': '14:45'},
    'B14': {'day': 'TUE', 'period': 4, 'start': '13:15', 'end': '14:45'},
    'C14': {'day': 'WED', 'period': 4, 'start': '13:15', 'end': '14:45'},
    'D14': {'day': 'THU', 'period': 4, 'start': '13:15', 'end': '14:45'},
    'E14': {'day': 'FRI', 'period': 4, 'start': '13:15', 'end': '14:45'},
    'F14': {'day': 'SAT', 'period': 4, 'start': '13:15', 'end': '14:45'},
    
    # Period 5: 14:50 - 16:20
    'A21': {'day': 'MON', 'period': 5, 'start': '14:50', 'end': '16:20'},
    'B21': {'day': 'TUE', 'period': 5, 'start': '14:50', 'end': '16:20'},
    'C21': {'day': 'WED', 'period': 5, 'start': '14:50', 'end': '16:20'},
    'D21': {'day': 'THU', 'period': 5, 'start': '14:50', 'end': '16:20'},
    'E21': {'day': 'FRI', 'period': 5, 'start': '14:50', 'end': '16:20'},
    'F21': {'day': 'SAT', 'period': 5, 'start': '14:50', 'end': '16:20'},
    
    # Period 6: 16:25 - 17:55
    'A22': {'day': 'MON', 'period': 6, 'start': '16:25', 'end': '17:55'},
    'B22': {'day': 'TUE', 'period': 6, 'start': '16:25', 'end': '17:55'},
    'C22': {'day': 'WED', 'period': 6, 'start': '16:25', 'end': '17:55'},
    'D22': {'day': 'THU', 'period': 6, 'start': '16:25', 'end': '17:55'},
    'E22': {'day': 'FRI', 'period': 6, 'start': '16:25', 'end': '17:55'},
    'F22': {'day': 'SAT', 'period': 6, 'start': '16:25', 'end': '17:55'},
    
    # Period 7: 18:00 - 19:30
    'A23': {'day': 'MON', 'period': 7, 'start': '18:00', 'end': '19:30'},
    'B23': {'day': 'TUE', 'period': 7, 'start': '18:00', 'end': '19:30'},
    'C23': {'day': 'WED', 'period': 7, 'start': '18:00', 'end': '19:30'},
    'D23': {'day': 'THU', 'period': 7, 'start': '18:00', 'end': '19:30'},
    'E23': {'day': 'FRI', 'period': 7, 'start': '18:00', 'end': '19:30'},
    'F23': {'day': 'SAT', 'period': 7, 'start': '18:00', 'end': '19:30'},
    
    # Period 8: 19:30 onwards (if needed)
    'A24': {'day': 'MON', 'period': 8, 'start': '19:30', 'end': '21:00'},
    'B24': {'day': 'TUE', 'period': 8, 'start': '19:30', 'end': '21:00'},
    'C24': {'day': 'WED', 'period': 8, 'start': '19:30', 'end': '21:00'},
    'D24': {'day': 'THU', 'period': 8, 'start': '19:30', 'end': '21:00'},
    'E24': {'day': 'FRI', 'period': 8, 'start': '19:30', 'end': '21:00'},
    'F24': {'day': 'SAT', 'period': 8, 'start': '19:30', 'end': '21:00'},
}


def get_slot_timing(slot_code):
    """Get timing info for a slot code."""
    return SLOT_TIMINGS.get(slot_code, None)
