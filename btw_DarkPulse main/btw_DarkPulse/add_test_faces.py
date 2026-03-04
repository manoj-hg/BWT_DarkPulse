import cv2
import os

def create_test_face():
    """Create a simple test face image for testing"""
    print("Creating test face image...")
    
    # Create a simple test image (you should replace this with real photos)
    # This is just to test the system
    test_image_path = os.path.join('dataset', 'TestStudent.jpg')
    
    # Check if dataset folder exists
    if not os.path.exists('dataset'):
        os.makedirs('dataset')
    
    # Try to capture a test frame from camera
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("Position your face in front of camera...")
        print("Press SPACE to capture, ESC to cancel")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.imshow('Capture Test Face - Press SPACE', frame)
            
            key = cv2.waitKey(1)
            if key == 32:  # SPACE key
                cv2.imwrite(test_image_path, frame)
                print(f"Test face saved to: {test_image_path}")
                break
            elif key == 27:  # ESC key
                print("Capture cancelled")
                break
        
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Could not open camera for test capture")
    
    return os.path.exists(test_image_path)

if __name__ == "__main__":
    if create_test_face():
        print("\nTest face created successfully!")
        print("Now run 'python app.py' and click 'Reload Faces'")
        print("Then click 'Start Attendance' to test recognition")
    else:
        print("\nFailed to create test face")
        print("Please manually add a photo to the dataset folder")
