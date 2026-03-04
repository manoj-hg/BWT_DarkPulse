try:
    from pymongo import MongoClient
    print("Testing MongoDB connection...")
    
    # Try to connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    
    # Test the connection
    client.server_info()
    print("SUCCESS: MongoDB is running and accessible!")
    
    # Test database creation
    db = client['attendance_db']
    test_collection = db['test']
    test_collection.insert_one({'test': 'connection'})
    test_collection.delete_many({})
    print("SUCCESS: Database operations working!")
    
    client.close()
    
except Exception as e:
    print(f"ERROR: MongoDB connection failed: {str(e)}")
    print("\nPlease make sure MongoDB is installed and running:")
    print("1. Download MongoDB from https://www.mongodb.com/try/download/community")
    print("2. Install and start MongoDB service")
    print("3. Try running this test again")
