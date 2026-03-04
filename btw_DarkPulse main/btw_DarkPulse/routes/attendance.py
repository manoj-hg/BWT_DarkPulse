from flask import Blueprint, request, jsonify
from services.improved_face_recognition import ImprovedFaceRecognitionService
from services.student_registration import StudentRegistrationService
from models.attendance import AttendanceModel
from datetime import date

# Create Blueprint
attendance_bp = Blueprint('attendance', __name__)

# Initialize services
face_service = ImprovedFaceRecognitionService()
registration_service = StudentRegistrationService()
attendance_model = AttendanceModel()

# Set attendance callback for face recognition
def mark_attendance_callback(student_name):
    """Callback function to mark attendance when face is recognized"""
    result = attendance_model.mark_attendance(student_name)
    return result

face_service.set_attendance_callback(mark_attendance_callback)

@attendance_bp.route('/start-attendance', methods=['POST'])
def start_attendance():
    """
    Start face recognition attendance system
    Expected JSON body: {}
    """
    try:
        # Check if face recognition is already running
        status = face_service.get_status()
        if status['is_running']:
            return jsonify({
                'success': False,
                'message': 'Face recognition is already running'
            }), 400
        
        # Check if known faces are loaded
        if status['known_faces_count'] == 0:
            return jsonify({
                'success': False,
                'message': 'No known faces found. Please add student images to dataset folder.'
            }), 400
        
        # Start face recognition
        result = face_service.start_recognition()
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Face recognition started successfully',
                'known_faces': status['known_faces'],
                'faces_count': status['known_faces_count']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting attendance: {str(e)}'
        }), 500

@attendance_bp.route('/stop-attendance', methods=['POST'])
def stop_attendance():
    """
    Stop face recognition attendance system
    Expected JSON body: {}
    """
    try:
        result = face_service.stop_recognition()
        
        return jsonify({
            'success': result['success'],
            'message': result['message']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error stopping attendance: {str(e)}'
        }), 500

@attendance_bp.route('/attendance-list', methods=['GET'])
def get_attendance_list():
    """
    Get list of attendance records
    Query parameters:
    - date: Filter by specific date (YYYY-MM-DD format)
    """
    try:
        # Get date filter from query parameters
        date_filter = request.args.get('date')
        
        # Validate date format if provided
        if date_filter:
            try:
                # Validate date format
                year, month, day = map(int, date_filter.split('-'))
                date(year, month, day)  # This will raise ValueError if invalid
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid date format. Use YYYY-MM-DD format.'
                }), 400
        
        # Get attendance records
        result = attendance_model.get_attendance_list(date_filter)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'count': result['count'],
                'date_filter': date_filter
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message'],
                'data': []
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching attendance list: {str(e)}',
            'data': []
        }), 500

@attendance_bp.route('/attendance-stats', methods=['GET'])
def get_attendance_stats():
    """
    Get attendance statistics
    """
    try:
        result = attendance_model.get_attendance_stats()
        
        if result['success']:
            return jsonify({
                'success': True,
                'stats': result['stats']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching stats: {str(e)}'
        }), 500

@attendance_bp.route('/mark-manual', methods=['POST'])
def mark_manual_attendance():
    """
    Manually mark attendance for a student
    Expected JSON body: {"student_name": "John Doe"}
    """
    try:
        data = request.get_json()
        
        if not data or 'student_name' not in data:
            return jsonify({
                'success': False,
                'message': 'Student name is required'
            }), 400
        
        student_name = data['student_name'].strip()
        
        if not student_name:
            return jsonify({
                'success': False,
                'message': 'Student name cannot be empty'
            }), 400
        
        # Mark attendance
        result = attendance_model.mark_attendance(student_name)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message'],
                'data': result['data']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error marking manual attendance: {str(e)}'
        }), 500

@attendance_bp.route('/recognition-status', methods=['GET'])
def get_recognition_status():
    """
    Get current status of face recognition service
    """
    try:
        status = face_service.get_status()
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting status: {str(e)}'
        }), 500

@attendance_bp.route('/reload-faces', methods=['POST'])
def reload_faces():
    """
    Reload known faces from dataset folder
    """
    try:
        # Stop recognition first if running
        if face_service.is_running:
            face_service.stop_recognition()
        
        # Reload faces
        result = face_service.reload_faces()
        
        if result:
            status = face_service.get_status()
            return jsonify({
                'success': True,
                'message': 'Faces reloaded successfully',
                'faces_count': status['known_faces_count'],
                'known_faces': status['known_faces']
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to reload faces'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error reloading faces: {str(e)}'
        }), 500

@attendance_bp.route('/register-student', methods=['POST'])
def register_student():
    """
    Register a new student with photo capture
    Expected JSON body: {"student_name": "John Doe"}
    """
    try:
        data = request.get_json()
        
        if not data or 'student_name' not in data:
            return jsonify({
                'success': False,
                'message': 'Student name is required'
            }), 400
        
        student_name = data['student_name'].strip()
        
        if not student_name:
            return jsonify({
                'success': False,
                'message': 'Student name cannot be empty'
            }), 400
        
        # Capture and save student photo
        result = registration_service.capture_student_photo(student_name)
        
        if result['success']:
            # Reload faces in the recognition service
            face_service.reload_faces()
            
            return jsonify({
                'success': True,
                'message': result['message'],
                'student_name': result['student_name'],
                'filepath': result['filepath']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error registering student: {str(e)}'
        }), 500

@attendance_bp.route('/registered-students', methods=['GET'])
def get_registered_students():
    """
    Get list of registered students
    """
    try:
        result = registration_service.get_registered_students()
        
        return jsonify({
            'success': result['success'],
            'students': result['students'],
            'count': result['count'],
            'message': result.get('message', '')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching registered students: {str(e)}',
            'students': []
        }), 500

@attendance_bp.route('/delete-student', methods=['POST'])
def delete_student():
    """
    Delete a registered student's photos
    Expected JSON body: {"student_name": "John Doe"}
    """
    try:
        data = request.get_json()
        
        if not data or 'student_name' not in data:
            return jsonify({
                'success': False,
                'message': 'Student name is required'
            }), 400
        
        student_name = data['student_name'].strip()
        
        if not student_name:
            return jsonify({
                'success': False,
                'message': 'Student name cannot be empty'
            }), 400
        
        # Delete student photos
        result = registration_service.delete_student_photo(student_name)
        
        if result['success']:
            # Reload faces in the recognition service
            face_service.reload_faces()
            
            return jsonify({
                'success': True,
                'message': result['message'],
                'deleted_files': result['deleted_files']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting student: {str(e)}'
        }), 500

@attendance_bp.route('/present-students', methods=['GET'])
def get_present_students():
    """
    Get list of students present today
    """
    try:
        today = date.today().isoformat()
        result = attendance_model.get_attendance_list(today)
        
        if result['success']:
            # Get unique student names
            present_students = list(set(record['student_name'] for record in result['data']))
            
            return jsonify({
                'success': True,
                'present_students': present_students,
                'count': len(present_students),
                'date': today
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message'],
                'present_students': []
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching present students: {str(e)}',
            'present_students': []
        }), 500

@attendance_bp.route('/clear-all-records', methods=['POST'])
def clear_all_records():
    """
    Clear ALL attendance records (for testing/demo purposes)
    """
    try:
        result = attendance_model.clear_all_records()
        
        return jsonify({
            'success': result['success'],
            'message': result['message']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error clearing all records: {str(e)}'
        }), 500

@attendance_bp.route('/clear-old-records', methods=['POST'])
def clear_old_records():
    """
    Clear attendance records older than specified days
    Expected JSON body: {"days": 30} (optional, defaults to 30)
    """
    try:
        data = request.get_json() or {}
        days = data.get('days', 30)
        
        if not isinstance(days, int) or days < 1:
            return jsonify({
                'success': False,
                'message': 'Days must be a positive integer'
            }), 400
        
        result = attendance_model.clear_old_records(days)
        
        return jsonify({
            'success': result['success'],
            'message': result['message']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error clearing old records: {str(e)}'
        }), 500
