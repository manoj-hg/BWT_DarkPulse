import cv2
import os
import numpy as np
from datetime import datetime
import threading

class StudentRegistrationService:
    """Service for registering new students with webcam capture"""
    
    def __init__(self, dataset_path='dataset'):
        self.dataset_path = dataset_path
        self.is_capturing = False
        self.camera = None
        
        # Ensure dataset folder exists
        if not os.path.exists(self.dataset_path):
            os.makedirs(self.dataset_path)
        
        # Load face cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def capture_student_photo(self, student_name):
        """
        Capture and save student photo from webcam
        Returns: {'success': bool, 'message': str, 'filepath': str}
        """
        try:
            # Validate student name
            if not student_name or not student_name.strip():
                return {
                    'success': False,
                    'message': 'Student name is required'
                }
            
            student_name = student_name.strip().replace(' ', '_')
            
            # Check if student already exists
            existing_files = []
            for ext in ['.jpg', '.jpeg', '.png']:
                filepath = os.path.join(self.dataset_path, f"{student_name}{ext}")
                if os.path.exists(filepath):
                    existing_files.append(filepath)
            
            if existing_files:
                return {
                    'success': False,
                    'message': f'Student "{student_name}" already exists',
                    'existing_files': existing_files
                }
            
            # Start camera capture
            result = self._capture_and_save(student_name)
            return result
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error capturing photo: {str(e)}'
            }
    
    def _capture_and_save(self, student_name):
        """Internal method to capture and save photo"""
        try:
            # Initialize camera
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                return {
                    'success': False,
                    'message': 'Could not open camera'
                }
            
            self.is_capturing = True
            print(f"Capturing photo for {student_name}...")
            print("Position your face in the frame and press SPACE to capture")
            print("Press ESC to cancel")
            
            captured = False
            saved_filepath = None
            
            while self.is_capturing:
                ret, frame = self.camera.read()
                if not ret:
                    break
                
                # Convert to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                
                # Draw face rectangles
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Add instructions
                cv2.putText(frame, "Press SPACE to capture, ESC to cancel", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.imshow('Student Registration - Capture Photo', frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == 32:  # SPACE key - capture photo
                    if len(faces) > 0:
                        # Save the photo
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{student_name}_{timestamp}.jpg"
                        filepath = os.path.join(self.dataset_path, filename)
                        
                        # Save the image
                        cv2.imwrite(filepath, frame)
                        saved_filepath = filepath
                        captured = True
                        
                        print(f"Photo saved: {filepath}")
                        break
                    else:
                        print("No face detected! Please position your face properly.")
                
                elif key == 27:  # ESC key - cancel
                    print("Capture cancelled")
                    break
            
            # Cleanup
            self.is_capturing = False
            if self.camera:
                self.camera.release()
            cv2.destroyAllWindows()
            
            if captured and saved_filepath:
                return {
                    'success': True,
                    'message': f'Successfully captured and saved photo for {student_name}',
                    'filepath': saved_filepath,
                    'student_name': student_name
                }
            else:
                return {
                    'success': False,
                    'message': 'Photo capture cancelled or failed'
                }
                
        except Exception as e:
            self.is_capturing = False
            if self.camera:
                self.camera.release()
            cv2.destroyAllWindows()
            return {
                'success': False,
                'message': f'Error during capture: {str(e)}'
            }
    
    def stop_capture(self):
        """Stop the capture process"""
        self.is_capturing = False
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
    
    def get_registered_students(self):
        """Get list of registered students"""
        try:
            students = []
            for filename in os.listdir(self.dataset_path):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    student_name = os.path.splitext(filename)[0]
                    # Remove timestamp if present
                    if '_' in student_name:
                        parts = student_name.split('_')
                        if len(parts) > 1 and parts[-1].isdigit():
                            student_name = '_'.join(parts[:-1])
                    students.append(student_name)
            
            return {
                'success': True,
                'students': list(set(students)),  # Remove duplicates
                'count': len(set(students))
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error getting students: {str(e)}',
                'students': []
            }
    
    def delete_student_photo(self, student_name):
        """Delete student photo(s)"""
        try:
            deleted_files = []
            
            # Find and delete all files for this student
            for filename in os.listdir(self.dataset_path):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    file_student_name = os.path.splitext(filename)[0]
                    # Remove timestamp if present
                    if '_' in file_student_name:
                        parts = file_student_name.split('_')
                        if len(parts) > 1 and parts[-1].isdigit():
                            file_student_name = '_'.join(parts[:-1])
                    
                    if file_student_name == student_name:
                        filepath = os.path.join(self.dataset_path, filename)
                        os.remove(filepath)
                        deleted_files.append(filename)
            
            if deleted_files:
                return {
                    'success': True,
                    'message': f'Deleted {len(deleted_files)} photo(s) for {student_name}',
                    'deleted_files': deleted_files
                }
            else:
                return {
                    'success': False,
                    'message': f'No photos found for student {student_name}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error deleting photos: {str(e)}'
            }
