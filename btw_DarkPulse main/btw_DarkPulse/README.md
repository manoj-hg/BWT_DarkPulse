# Face Recognition Attendance System

A complete automated attendance system using face recognition technology built with Python, Flask, and OpenCV.

## Features

- **Face Recognition**: Automatic face detection and recognition using OpenCV and face_recognition library
- **Live Webcam Feed**: Real-time face detection from webcam
- **Automatic Attendance Marking**: Automatically marks attendance when a recognized face is detected
- **Duplicate Prevention**: Prevents duplicate attendance entries for the same day
- **Web Dashboard**: Simple and intuitive web interface
- **REST APIs**: Clean API endpoints for integration
- **MongoDB Storage**: Secure and scalable data storage
- **Manual Attendance**: Option to manually mark attendance
- **Attendance Statistics**: View attendance stats and records

## Project Structure

```
face-recognition-attendance/
├── app.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── dataset/               # Student face images
├── models/                # Database models
│   └── attendance.py      # MongoDB attendance model
├── services/              # Business logic
│   └── face_recognition.py # Face recognition service
├── routes/                # API routes
│   └── attendance.py      # Attendance API endpoints
├── static/                # Static files
│   ├── css/
│   │   └── style.css      # Styling
│   └── js/
│       └── script.js      # Frontend JavaScript
└── templates/             # HTML templates
    └── index.html         # Main dashboard
```

## Prerequisites

- Python 3.7 or higher
- MongoDB installed and running
- Webcam (for face recognition)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd face-recognition-attendance
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install MongoDB

**Windows:**
- Download and install MongoDB from [official website](https://www.mongodb.com/try/download/community)
- Start MongoDB service

**macOS:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu):**
```bash
sudo apt update
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### 5. Setup Student Dataset

1. Add student face images to the `dataset/` folder
2. Image naming format: `StudentName.jpg` or `StudentName.png`
3. Example: `JohnDoe.jpg`, `JaneSmith.png`

**Important:**
- Use clear, front-facing photos
- One face per image
- Good lighting conditions
- High resolution images work better

## Running the Application

### 1. Start MongoDB

Make sure MongoDB is running on your system.

### 2. Run the Flask Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

### 3. Access the Web Dashboard

Open your web browser and navigate to `http://localhost:5000`

## Usage Instructions

### 1. Prepare Student Faces

- Add student images to the `dataset/` folder
- Click "Reload Faces" button to load new faces
- Verify face count in the dashboard

### 2. Start Attendance System

1. Click "Start Attendance" button
2. Allow webcam access when prompted
3. Face recognition window will open
4. Students face the camera for automatic attendance
5. Press 'q' in the recognition window to stop

### 3. View Attendance Records

- Attendance records appear in real-time
- Filter by date using the date picker
- View statistics in the status cards

### 4. Manual Attendance

- Use the manual attendance section
- Enter student name and click "Mark Attendance"
- Useful for backup when face recognition fails

## API Endpoints

### Attendance Control

- `POST /api/start-attendance` - Start face recognition
- `POST /api/stop-attendance` - Stop face recognition
- `GET /api/recognition-status` - Get system status
- `POST /api/reload-faces` - Reload known faces

### Attendance Management

- `GET /api/attendance-list` - Get attendance records
- `GET /api/attendance-list?date=YYYY-MM-DD` - Get records for specific date
- `POST /api/mark-manual` - Mark manual attendance
- `GET /api/attendance-stats` - Get attendance statistics
- `POST /api/clear-old-records` - Clear old records

### System

- `GET /health` - Health check endpoint

## Configuration

### MongoDB Connection

Default connection: `mongodb://localhost:27017/attendance_db`

To change database connection, modify in `app.py`:
```python
app.config['MONGO_URI'] = 'mongodb://localhost:27017/your_database'
```

### Face Recognition Settings

Modify tolerance in `services/face_recognition.py`:
```python
matches = face_recognition.compare_faces(
    self.known_face_encodings, 
    face_encoding, 
    tolerance=0.6  # Adjust this value (0.4-0.7)
)
```

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running
   - Check connection string in app.py
   - Verify MongoDB is accessible on localhost:27017

2. **No Faces Detected**
   - Check dataset folder contains images
   - Verify image format (jpg, jpeg, png)
   - Ensure images have clear faces
   - Click "Reload Faces" button

3. **Webcam Not Working**
   - Check webcam permissions
   - Ensure no other application is using webcam
   - Try restarting the application

4. **Face Recognition Not Accurate**
   - Add better quality images to dataset
   - Improve lighting conditions
   - Adjust tolerance value in face_recognition.py
   - Use multiple images per student if needed

5. **Dependencies Installation Issues**

**Windows:**
```bash
# If face-recognition fails to install, try:
pip install --no-cache-dir face-recognition
# Or install cmake first:
pip install cmake
pip install dlib
pip install face-recognition
```

**macOS:**
```bash
# Install Xcode command line tools
xcode-select --install
# Then install dependencies
pip install -r requirements.txt
```

**Linux:**
```bash
# Install required system packages
sudo apt update
sudo apt install build-essential cmake
sudo apt install libopenblas-dev liblapack-dev
sudo apt install libx11-dev libgtk-3-dev
# Then install Python packages
pip install -r requirements.txt
```

## Performance Tips

1. **Optimize Face Recognition**
   - Use smaller image sizes for faster processing
   - Limit the number of known faces
   - Adjust frame rate in recognition loop

2. **Database Optimization**
   - Create indexes on frequently queried fields
   - Regularly clean old attendance records
   - Use connection pooling for production

3. **System Resources**
   - Close unnecessary applications
   - Ensure sufficient RAM available
   - Use SSD for better database performance

## Security Considerations

1. **Data Privacy**
   - Store face images securely
   - Implement proper access controls
   - Consider encrypting sensitive data

2. **Network Security**
   - Use HTTPS in production
   - Implement authentication
   - Validate all user inputs

3. **System Security**
   - Regular security updates
   - Firewall configuration
   - Monitor access logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository
4. Contact the development team

## Future Enhancements

- [ ] Multi-camera support
- [ ] Mobile app interface
- [ ] Advanced analytics dashboard
- [ ] Email notifications
- [ ] Export attendance reports
- [ ] Integration with student management systems
- [ ] Cloud deployment support
- [ ] Advanced anti-spoofing measures

---

**Note**: This project is designed for educational and demonstration purposes. For production use, additional security measures and testing are recommended.
