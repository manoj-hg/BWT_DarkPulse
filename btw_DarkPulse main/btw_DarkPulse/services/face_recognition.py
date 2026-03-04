import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import threading
import time

class FaceRecognitionService:
    """Service for face recognition using OpenCV and face_recognition library"""
    
    def __init__(self, dataset_path='dataset'):
        self.dataset_path = dataset_path
        self.known_face_encodings = []
        self.known_face_names = []
        self.is_running = False
        self.camera = None
        self.attendance_callback = None
        
        # Load known faces from dataset
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load known faces from dataset folder"""
        try:
            print("Loading known faces...")
            
            if not os.path.exists(self.dataset_path):
                print(f"Dataset folder '{self.dataset_path}' not found!")
                return False
            
            # Iterate through all files in dataset folder
            for filename in os.listdir(self.dataset_path):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    # Extract student name from filename (without extension)
                    student_name = os.path.splitext(filename)[0]
                    image_path = os.path.join(self.dataset_path, filename)
                    
                    # Load image and encode face
                    image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(image)
                    
                    if len(face_encodings) > 0:
                        # Use first face found in the image
                        face_encoding = face_encodings[0]
                        self.known_face_encodings.append(face_encoding)
                        self.known_face_names.append(student_name)
                        print(f"Loaded face for: {student_name}")
                    else:
                        print(f"No face found in image: {filename}")
            
            print(f"Successfully loaded {len(self.known_face_names)} faces")
            return True
            
        except Exception as e:
            print(f"Error loading faces: {str(e)}")
            return False
    
    def set_attendance_callback(self, callback):
        """Set callback function for marking attendance"""
        self.attendance_callback = callback
    
    def start_recognition(self):
        """Start face recognition from webcam"""
        if self.is_running:
            return {'success': False, 'message': 'Recognition already running'}
        
        if len(self.known_face_encodings) == 0:
            return {'success': False, 'message': 'No known faces loaded'}
        
        # Start recognition in a separate thread
        recognition_thread = threading.Thread(target=self._recognition_loop)
        recognition_thread.daemon = True
        recognition_thread.start()
        
        return {'success': True, 'message': 'Face recognition started'}
    
    def stop_recognition(self):
        """Stop face recognition"""
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
        cv2.destroyAllWindows()
        return {'success': True, 'message': 'Face recognition stopped'}
    
    def _recognition_loop(self):
        """Main recognition loop running in separate thread"""
        try:
            self.is_running = True
            
            # Initialize webcam
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("Error: Could not open webcam")
                self.is_running = False
                return
            
            print("Face recognition started. Press 'q' to stop.")
            
            # Track recently recognized faces to avoid duplicate marking
            recently_recognized = {}
            cooldown_period = 30  # seconds
            
            while self.is_running:
                ret, frame = self.camera.read()
                if not ret:
                    print("Error: Could not read from webcam")
                    break
                
                # Resize frame for faster processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                # Find all face locations and encodings in current frame
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                # Process each face found
                for face_encoding in face_encodings:
                    # Compare with known faces
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, 
                        face_encoding, 
                        tolerance=0.6
                    )
                    
                    face_distances = face_recognition.face_distance(
                        self.known_face_encodings, 
                        face_encoding
                    )
                    
                    name = "Unknown"
                    
                    # Find best match
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index]
                    
                    # If face is recognized and not recently marked
                    if name != "Unknown":
                        current_time = time.time()
                        
                        # Check if this person was recently recognized
                        if (name not in recently_recognized or 
                            current_time - recently_recognized[name] > cooldown_period):
                            
                            # Mark attendance
                            if self.attendance_callback:
                                result = self.attendance_callback(name)
                                print(f"Attendance result for {name}: {result}")
                            
                            # Update recently recognized
                            recently_recognized[name] = current_time
                            
                            # Draw rectangle and name on frame
                            self._draw_face_info(frame, face_locations[0], name, True)
                        else:
                            # Draw rectangle but don't mark attendance again
                            self._draw_face_info(frame, face_locations[0], name, False)
                    else:
                        # Draw rectangle for unknown face
                        if len(face_locations) > 0:
                            self._draw_face_info(frame, face_locations[0], "Unknown", False)
                
                # Display the resulting frame
                cv2.imshow('Face Recognition Attendance', frame)
                
                # Break loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Cleanup
            self.stop_recognition()
            
        except Exception as e:
            print(f"Error in recognition loop: {str(e)}")
            self.is_running = False
    
    def _draw_face_info(self, frame, face_location, name, marked_attendance):
        """Draw face rectangle and name information on frame"""
        try:
            # Scale face location back to original frame size
            top, right, bottom, left = [coord * 4 for coord in face_location]
            
            # Choose color based on whether attendance was marked
            if marked_attendance:
                color = (0, 255, 0)  # Green for marked attendance
            elif name == "Unknown":
                color = (0, 0, 255)  # Red for unknown
            else:
                color = (255, 0, 0)  # Blue for recognized but cooldown
            
            # Draw rectangle around face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label with name
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            
            if marked_attendance:
                label = f"{name} - Marked!"
            else:
                label = name
            
            cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
            
        except Exception as e:
            print(f"Error drawing face info: {str(e)}")
    
    def get_status(self):
        """Get current status of face recognition service"""
        return {
            'is_running': self.is_running,
            'known_faces_count': len(self.known_face_names),
            'known_faces': self.known_face_names.copy()
        }
    
    def reload_faces(self):
        """Reload known faces from dataset"""
        self.known_face_encodings = []
        self.known_face_names = []
        return self.load_known_faces()
