"""Seed data script to populate the database with sample VIT courses."""

from models import db, Course, Faculty, Slot, Registration


def seed_database():
    """Populate database with sample data from DIFFERENTIAL.html."""
    
    # Clear existing data
    Registration.query.delete()
    Slot.query.delete()
    Faculty.query.delete()
    Course.query.delete()
    
    # Create Faculties
    faculties_data = [
        {'name': 'MANISHA JAIN', 'department': 'MATH'},
        {'name': 'MAMTA AGRAWAL', 'department': 'MATH'},
        {'name': 'SHEERIN KAYENAT', 'department': 'MATH'},
        {'name': 'BHUMIKA CHOKSI', 'department': 'MATH'},
        {'name': 'RAHUL KUMAR CHATURVEDI', 'department': 'MATH'},
        {'name': 'MAYANK SHARMA', 'department': 'MATH'},
        {'name': 'PAVAN KUMAR', 'department': 'MATH'},
        {'name': 'UDAI KUMAR', 'department': 'MATH'},
        {'name': 'ZAHEER KAREEM', 'department': 'MATH'},
        {'name': 'FEEROZ', 'department': 'MATH'},
        {'name': 'SWATI CHAUHAN', 'department': 'MATH'},
        {'name': 'BENEVATHO JAISON A', 'department': 'MATH'},
        {'name': 'UJJWAL KUMAR MISHRA', 'department': 'MATH'},
        {'name': 'ANAND KUMAR', 'department': 'CSE'},
        {'name': 'PRIYA SHARMA', 'department': 'CSE'},
        {'name': 'RAJESH VERMA', 'department': 'CSE'},
        {'name': 'SUNITA GUPTA', 'department': 'CSE'},
        {'name': 'AMIT SINGH', 'department': 'SCOPE'},
        {'name': 'NEHA PATEL', 'department': 'SCOPE'},
        {'name': 'VIKRAM THAKUR', 'department': 'SCOPE'},
    ]
    
    faculties = {}
    for f_data in faculties_data:
        faculty = Faculty(**f_data)
        db.session.add(faculty)
        db.session.flush()
        faculties[f_data['name']] = faculty
    
    # Create Courses
    courses_data = [
        {
            'code': 'MAT2001',
            'name': 'Differential And Difference Equations',
            'l': 2, 't': 1, 'p': 0, 'j': 0, 'c': 3,
            'course_type': 'LT',
            'category': 'UENSE'
        },
        {
            'code': 'CSA4028',
            'name': 'Machine Learning',
            'l': 3, 't': 0, 'p': 2, 'j': 0, 'c': 4,
            'course_type': 'LTP',
            'category': 'PC'
        },
        {
            'code': 'CSE3010',
            'name': 'Operating Systems',
            'l': 3, 't': 0, 'p': 2, 'j': 0, 'c': 4,
            'course_type': 'LP',
            'category': 'PC'
        },
        {
            'code': 'CSA3006',
            'name': 'Data Structures and Algorithms',
            'l': 3, 't': 0, 'p': 2, 'j': 0, 'c': 4,
            'course_type': 'LTP',
            'category': 'PC'
        },
        {
            'code': 'HUM1002',
            'name': 'Effective Technical Communication',
            'l': 2, 't': 0, 'p': 0, 'j': 0, 'c': 2,
            'course_type': 'LT',
            'category': 'UC'
        },
        {
            'code': 'MAT2003',
            'name': 'Linear Algebra',
            'l': 2, 't': 1, 'p': 0, 'j': 0, 'c': 3,
            'course_type': 'LT',
            'category': 'UENSE'
        },
        {
            'code': 'CSA4029',
            'name': 'Deep Learning',
            'l': 3, 't': 0, 'p': 2, 'j': 0, 'c': 4,
            'course_type': 'LTP',
            'category': 'PC'
        },
        {
            'code': 'CSA3007',
            'name': 'Computer Networks',
            'l': 3, 't': 0, 'p': 2, 'j': 0, 'c': 4,
            'course_type': 'LTP',
            'category': 'PC'
        },
        {
            'code': 'PLA1006',
            'name': 'Digital Logic Design',
            'l': 2, 't': 0, 'p': 2, 'j': 0, 'c': 3,
            'course_type': 'LP',
            'category': 'PC'
        },
    ]
    
    courses = {}
    for c_data in courses_data:
        course = Course(**c_data)
        db.session.add(course)
        db.session.flush()
        courses[c_data['code']] = course
    
    # Create Slots (based on DIFFERENTIAL.html data)
    slots_data = [
        # MAT2001 slots
        {'slot_code': 'A11+A12', 'course': 'MAT2001', 'faculty': 'MANISHA JAIN', 'venue': 'CR-011', 'available': 60},
        {'slot_code': 'A12+A13', 'course': 'MAT2001', 'faculty': 'MAMTA AGRAWAL', 'venue': 'CR-013', 'available': 55},
        {'slot_code': 'A14+D11', 'course': 'MAT2001', 'faculty': 'SHEERIN KAYENAT', 'venue': 'CR-008', 'available': 62},
        {'slot_code': 'A21+A22', 'course': 'MAT2001', 'faculty': 'BHUMIKA CHOKSI', 'venue': 'CR-028', 'available': 64},
        {'slot_code': 'A21+A22', 'course': 'MAT2001', 'faculty': 'RAHUL KUMAR CHATURVEDI', 'venue': 'CR-031', 'available': 65},
        {'slot_code': 'B11+B12', 'course': 'MAT2001', 'faculty': 'SHEERIN KAYENAT', 'venue': 'CR-014', 'available': 37},
        {'slot_code': 'B11+B12', 'course': 'MAT2001', 'faculty': 'MAYANK SHARMA', 'venue': 'CR-017', 'available': 59},
        {'slot_code': 'B21+E14', 'course': 'MAT2001', 'faculty': 'PAVAN KUMAR', 'venue': 'CR-012', 'available': 62},
        {'slot_code': 'B22+F21', 'course': 'MAT2001', 'faculty': 'PAVAN KUMAR', 'venue': 'CR-009', 'available': 61},
        {'slot_code': 'B22+F21', 'course': 'MAT2001', 'faculty': 'UDAI KUMAR', 'venue': 'CR-010', 'available': 56},
        {'slot_code': 'C11+C12', 'course': 'MAT2001', 'faculty': 'ZAHEER KAREEM', 'venue': 'CR-026', 'available': 56},
        {'slot_code': 'C11+C12', 'course': 'MAT2001', 'faculty': 'FEEROZ', 'venue': 'CR-027', 'available': 45},
        {'slot_code': 'C11+C12', 'course': 'MAT2001', 'faculty': 'SWATI CHAUHAN', 'venue': 'CR-030', 'available': 61},
        {'slot_code': 'D11+D12', 'course': 'MAT2001', 'faculty': 'ZAHEER KAREEM', 'venue': 'CR-002', 'available': 60},
        {'slot_code': 'D21+D22', 'course': 'MAT2001', 'faculty': 'MANISHA JAIN', 'venue': 'CR-021', 'available': 69},
        {'slot_code': 'D21+D22', 'course': 'MAT2001', 'faculty': 'MAYANK SHARMA', 'venue': 'CR-022', 'available': 65},
        {'slot_code': 'E11+E12', 'course': 'MAT2001', 'faculty': 'UJJWAL KUMAR MISHRA', 'venue': 'CR-019', 'available': 59},
        {'slot_code': 'E11+E12', 'course': 'MAT2001', 'faculty': 'MAMTA AGRAWAL', 'venue': 'CR-020', 'available': 25},
        {'slot_code': 'E14+E22', 'course': 'MAT2001', 'faculty': 'BHUMIKA CHOKSI', 'venue': 'CR-007', 'available': 60},
        
        # CSA4028 slots
        {'slot_code': 'E11+E12', 'course': 'CSA4028', 'faculty': 'ANAND KUMAR', 'venue': 'AB02-316', 'available': 45},
        {'slot_code': 'C14+A21', 'course': 'CSA4028', 'faculty': 'PRIYA SHARMA', 'venue': 'AB02-316', 'available': 50},
        
        # CSE3010 slots
        {'slot_code': 'F11+F12', 'course': 'CSE3010', 'faculty': 'RAJESH VERMA', 'venue': 'AB02-330', 'available': 42},
        {'slot_code': 'F12+F13', 'course': 'CSE3010', 'faculty': 'SUNITA GUPTA', 'venue': 'AB02-330', 'available': 38},
        
        # CSA3006 slots
        {'slot_code': 'A21+A22', 'course': 'CSA3006', 'faculty': 'AMIT SINGH', 'venue': 'AB02-330', 'available': 55},
        {'slot_code': 'A22+A23', 'course': 'CSA3006', 'faculty': 'AMIT SINGH', 'venue': 'AB02-330', 'available': 48},
        {'slot_code': 'C21+C22', 'course': 'CSA3006', 'faculty': 'NEHA PATEL', 'venue': 'AB02-330', 'available': 52},
        
        # HUM1002 slots
        {'slot_code': 'A14+A21', 'course': 'HUM1002', 'faculty': 'VIKRAM THAKUR', 'venue': 'AB-516', 'available': 65},
        {'slot_code': 'B14+B21', 'course': 'HUM1002', 'faculty': 'VIKRAM THAKUR', 'venue': 'AB-516', 'available': 58},
        
        # MAT2003 slots
        {'slot_code': 'B21+B22', 'course': 'MAT2003', 'faculty': 'MANISHA JAIN', 'venue': 'CR-021', 'available': 55},
        {'slot_code': 'C21+A24', 'course': 'MAT2003', 'faculty': 'BENEVATHO JAISON A', 'venue': 'CR-009', 'available': 53},
        
        # CSA4029 slots
        {'slot_code': 'E21+E22', 'course': 'CSA4029', 'faculty': 'ANAND KUMAR', 'venue': 'AB02-423', 'available': 40},
        {'slot_code': 'F21+F22', 'course': 'CSA4029', 'faculty': 'ANAND KUMAR', 'venue': 'AB02-423', 'available': 35},
        
        # CSA3007 slots
        {'slot_code': 'B22+B23', 'course': 'CSA3007', 'faculty': 'PRIYA SHARMA', 'venue': 'AB02-423', 'available': 48},
        {'slot_code': 'A24+B24', 'course': 'CSA3007', 'faculty': 'RAJESH VERMA', 'venue': 'AB02-423', 'available': 42},
        
        # PLA1006 slots
        {'slot_code': 'E22+F22', 'course': 'PLA1006', 'faculty': 'SUNITA GUPTA', 'venue': 'AB02-217', 'available': 50},
    ]
    
    for s_data in slots_data:
        course = courses.get(s_data['course'])
        faculty = faculties.get(s_data['faculty'])
        
        if course and faculty:
            slot = Slot(
                slot_code=s_data['slot_code'],
                course_id=course.id,
                faculty_id=faculty.id,
                venue=s_data['venue'],
                available_seats=s_data['available'],
                total_seats=70
            )
            db.session.add(slot)
    
    db.session.commit()
    print("Database seeded successfully!")


if __name__ == '__main__':
    from app import app
    from models import Registration
    
    with app.app_context():
        seed_database()
