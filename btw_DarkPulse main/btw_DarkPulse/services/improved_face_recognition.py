import cv2
import os
import numpy as np
from datetime import datetime
import threading
import time
import pickle

class ImprovedFaceRecognitionService:
    """Improved face recognition service with better matching algorithm"""
    
    def __init__(self, dataset_path='dataset'):
        self.dataset_path = dataset_path
        self.known_faces = {}
        self.is_running = False
        self.camera = None
        self.attendance_callback = None
        
        # Load face cascade classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Load known faces from dataset
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load known faces from dataset folder using improved face detection"""
        try:
            print("Loading known faces...")
            
            if not os.path.exists(self.dataset_path):
                print(f"Dataset folder '{self.dataset_path}' not found!")
                return False
            
            # Try to load existing face data
            if os.path.exists('known_faces_improved.pkl'):
                try:
                    with open('known_faces_improved.pkl', 'rb') as f:
                        self.known_faces = pickle.load(f)
                    print(f"Loaded {len(self.known_faces)} known faces from cache")
                    return True
                except:
                    print("Could not load cached face data, rebuilding...")
            
            # Iterate through all files in dataset folder
            for filename in os.listdir(self.dataset_path):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    # Extract student name from filename (without extension)
                    student_name = os.path.splitext(filename)[0]
                    image_path = os.path.join(self.dataset_path, filename)
                    
                    # Load image and detect face
                    image = cv2.imread(image_path)
                    if image is None:
                        print(f"Could not load image: {filename}")
                        continue
                    
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                    
                    if len(faces) > 0:
                        # Use the largest face found
                        largest_face = max(faces, key=lambda x: x[2] * x[3])
                        (x, y, w, h) = largest_face
                        face_roi = gray[y:y+h, x:x+w]
                        
                        # Resize to standard size for comparison
                        face_roi = cv2.resize(face_roi, (100, 100))
                        
                        # Store face data with additional features
                        self.known_faces[student_name] = {
                            'face_data': face_roi,
                            'bbox': (x, y, w, h),
                            'histogram': cv2.calcHist([face_roi], [0], None, [256], [0, 256])
                        }
                        print(f"Loaded face for: {student_name}")
                    else:
                        print(f"No face found in image: {filename}")
            
            # Save to cache
            try:
                with open('known_faces_improved.pkl', 'wb') as f:
                    pickle.dump(self.known_faces, f)
            except:
                print("Could not save face data cache")
            
            print(f"Successfully loaded {len(self.known_faces)} faces")
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
        
        if len(self.known_faces) == 0:
            return {'success': False, 'message': 'No known faces loaded'}
        
        # Start recognition in a separate thread
        recognition_thread = threading.Thread(target=self._recognition_loop)
        recognition_thread.daemon = True
        recognition_thread.start()
        
        return {'success': True, 'message': 'Face recognition started'}
    
    def stop_recognition(self):
        """Stop face recognition"""
        print("Stopping face recognition...")
        self.is_running = False
        
        # Close camera
        if self.camera:
            self.camera.release()
            self.camera = None
            print("Camera released")
        
        # Close all OpenCV windows
        cv2.destroyAllWindows()
        print("OpenCV windows closed")
        
        return {'success': True, 'message': 'Face recognition stopped'}
    
    def _compare_faces(self, face_roi, known_face_data):
        """Compare faces using multiple methods for better accuracy"""
        try:
            # Method 1: Template matching
            result = cv2.matchTemplate(face_roi, known_face_data['face_data'], cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            template_score = max_val
            
            # Method 2: Histogram comparison
            face_hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
            hist_score = cv2.compareHist(known_face_data['histogram'], face_hist, cv2.HISTCMP_CORREL)
            
            # Method 3: Structural Similarity (simplified)
            diff = cv2.absdiff(face_roi, known_face_data['face_data'])
            diff_score = 1 - (np.sum(diff) / (face_roi.size * 255))
            
            # Combine scores (weighted average)
            combined_score = (template_score * 0.5 + hist_score * 0.3 + diff_score * 0.2)
            
            return combined_score
            
        except Exception as e:
            print(f"Error in face comparison: {str(e)}")
            return 0
    
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
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces in the frame
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                
                recognized_name = "Unknown"
                best_match_score = 0
                
                # Process each face found
                for (x, y, w, h) in faces:
                    # Extract face ROI
                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (100, 100))
                    
                    # Compare with known faces
                    best_match = None
                    best_score = 0
                    
                    for name, face_data in self.known_faces.items():
                        score = self._compare_faces(face_roi, face_data)
                        
                        # Lower threshold for better recognition
                        if score > best_score and score > 0.3:  # Lowered threshold
                            best_score = score
                            best_match = name
                    
                    if best_match:
                        recognized_name = best_match
                        best_match_score = best_score
                        
                        # Check if this person was recently recognized
                        current_time = time.time()
                        if (best_match not in recently_recognized or 
                            current_time - recently_recognized[best_match] > cooldown_period):
                            
                            # Mark attendance
                            if self.attendance_callback:
                                result = self.attendance_callback(best_match)
                                print(f"Attendance result for {best_match}: {result}")
                                print(f"Match confidence: {best_score:.2f}")
                            
                            # Update recently recognized
                            recently_recognized[best_match] = current_time
                            
                            # Draw rectangle and name on frame
                            self._draw_face_info(frame, x, y, w, h, best_match, True, best_score)
                        else:
                            # Draw rectangle but don't mark attendance again
                            self._draw_face_info(frame, x, y, w, h, best_match, False, best_score)
                    else:
                        # Draw rectangle for unknown face
                        self._draw_face_info(frame, x, y, w, h, "Unknown", False, 0)
                
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
    
    def _draw_face_info(self, frame, x, y, w, h, name, marked_attendance, confidence=0):
        """Draw face rectangle and name information on frame"""
        try:
            # Choose color based on whether attendance was marked
            if marked_attendance:
                color = (0, 255, 0)  # Green for marked attendance
            elif name == "Unknown":
                color = (0, 0, 255)  # Red for unknown
            else:
                color = (255, 0, 0)  # Blue for recognized but cooldown
            
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Draw label with name and confidence
            cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            
            if marked_attendance:
                label = f"{name} - Marked!"
            elif confidence > 0:
                label = f"{name} ({confidence:.2f})"
            else:
                label = name
            
            cv2.putText(frame, label, (x + 6, y - 6), font, 0.8, (255, 255, 255), 1)
            
        except Exception as e:
            print(f"Error drawing face info: {str(e)}")
    
    def get_status(self):
        """Get current status of face recognition service"""
        return {
            'is_running': self.is_running,
            'known_faces_count': len(self.known_faces),
            'known_faces': list(self.known_faces.keys())
        }
    
    def reload_faces(self):
        """Reload known faces from dataset"""
        self.known_faces = {}
        # Remove cache file to force reload
        if os.path.exists('known_faces_improved.pkl'):
            os.remove('known_faces_improved.pkl')
        return self.load_known_faces()
