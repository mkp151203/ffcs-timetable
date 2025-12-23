from .database import db
from .course import Course
from .faculty import Faculty
from .slot import Slot
from .registration import Registration

from .user import User

__all__ = ['db', 'Course', 'Faculty', 'Slot', 'Registration', 'User']
