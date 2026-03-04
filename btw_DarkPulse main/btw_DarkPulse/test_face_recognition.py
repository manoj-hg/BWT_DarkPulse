from services.simple_face_recognition import SimpleFaceRecognitionService

def test_face_recognition():
    print("=== Face Recognition Test ===")
    print()
    
    # Initialize service
    service = SimpleFaceRecognitionService()
    
    # Check status
    status = service.get_status()
    print(f"Known faces loaded: {status['known_faces_count']}")
    print(f"Known faces: {status['known_faces']}")
    
    if status['known_faces_count'] == 0:
        print()
        print("WARNING: No faces loaded!")
        print("Please add student photos to the 'dataset' folder")
        print("Name files like: JohnDoe.jpg, JaneSmith.png")
        print("Then click 'Reload Faces' in the web dashboard")
        return False
    
    print()
    print("Testing face recognition startup...")
    result = service.start_recognition()
    
    if result['success']:
        print("SUCCESS: Face recognition started!")
        print("Camera window should open...")
        print("Press 'q' in the camera window to stop")
        print()
        print("If you see the camera feed, everything is working!")
        print("The face recognition will try to match faces with known students.")
        
        # Keep it running for a few seconds to test
        import time
        time.sleep(5)
        
        # Stop it
        service.stop_recognition()
        print("Test completed successfully!")
        return True
    else:
        print(f"ERROR: {result['message']}")
        return False

if __name__ == "__main__":
    test_face_recognition()
