import cv2

def check_camera_permissions():
    """Check and help fix camera permission issues"""
    
    print("=== Camera Permission Checker ===")
    print()
    
    # Check if camera can be accessed
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Camera cannot be accessed!")
        print()
        print("SOLUTIONS:")
        print("1. Close all other apps using camera (Zoom, Teams, Skype, etc.)")
        print("2. Check Windows Camera Privacy Settings:")
        print("   - Go to Settings > Privacy > Camera")
        print("   - Make sure 'Camera access' is ON")
        print("   - Make sure 'Allow apps to access your camera' is ON")
        print("3. Restart your computer")
        print("4. Try running the application as Administrator")
        print("5. Check if camera is properly connected")
        return False
    
    print("SUCCESS: Camera is accessible!")
    
    # Try to read a frame
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Camera can be opened but cannot read frames!")
        cap.release()
        return False
    
    print("SUCCESS: Camera can capture frames!")
    print(f"SUCCESS: Camera resolution: {frame.shape[1]}x{frame.shape[0]}")
    
    cap.release()
    return True

if __name__ == "__main__":
    if check_camera_permissions():
        print("\nCamera is working! You can now run the attendance system.")
    else:
        print("\nFix the camera issues above and try again.")
