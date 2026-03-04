import cv2
import time

print("Testing camera access...")
print("Make sure no other application is using your camera (Zoom, Teams, etc.)")
print("Press 'q' to close the camera test")
print()

try:
    # Try to open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Could not open camera!")
        print("Possible solutions:")
        print("1. Close other applications using camera")
        print("2. Check camera permissions")
        print("3. Restart your computer")
        print("4. Check if camera is properly connected")
        exit()
    
    print("SUCCESS: Camera opened!")
    print("Camera test window should appear...")
    print("If you see your camera feed, camera is working properly!")
    
    # Test camera for 10 seconds
    start_time = time.time()
    while time.time() - start_time < 10:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Could not read from camera!")
            break
        
        # Add text to frame
        cv2.putText(frame, "Camera Test - Press 'q' to close", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Camera Test', frame)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Camera test completed!")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    print("\nTroubleshooting steps:")
    print("1. Allow camera access when prompted")
    print("2. Check Windows camera privacy settings")
    print("3. Restart the application")
    print("4. Try running as administrator")
