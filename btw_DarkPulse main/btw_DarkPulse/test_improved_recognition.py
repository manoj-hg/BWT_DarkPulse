from services.improved_face_recognition import ImprovedFaceRecognitionService

def test_improved_recognition():
    print("=== Testing Improved Face Recognition ===")
    print()
    
    # Initialize service
    service = ImprovedFaceRecognitionService()
    
    # Check status
    status = service.get_status()
    print(f"Known faces loaded: {status['known_faces_count']}")
    print(f"Known faces: {status['known_faces']}")
    
    if status['known_faces_count'] == 0:
        print("No faces loaded!")
        return False
    
    print()
    print("Starting improved face recognition...")
    print("This should now recognize faces better!")
    print("Press 'q' to stop")
    print()
    
    result = service.start_recognition()
    
    if result['success']:
        print("SUCCESS: Improved face recognition started!")
        print("The system should now recognize your faces!")
        print("Look for confidence scores in the labels")
        
        # Keep it running for testing
        import time
        try:
            time.sleep(10)  # Run for 10 seconds
        except KeyboardInterrupt:
            pass
        
        # Stop it
        service.stop_recognition()
        print("Test completed!")
        return True
    else:
        print(f"ERROR: {result['message']}")
        return False

if __name__ == "__main__":
    test_improved_recognition()
