# Quick Setup Guide - Face Recognition Attendance System

## 🚀 How to Run the System

### Method 1: Easy Start (Recommended)

1. **Double-click the `run.bat` file** in your project folder
2. Wait for the setup to complete
3. Open your browser and go to: http://localhost:5000

### Method 2: Manual Start

1. **Open PowerShell or Command Prompt** in your project folder
2. Run: `python app.py`
3. Open browser and go to: http://localhost:5000

## 📋 What You Need to Do First

### 1. Add Student Photos
- Put student photos in the `dataset/` folder
- Name files like: `JohnDoe.jpg`, `JaneSmith.png`
- Use clear, front-facing photos

### 2. Start MongoDB (if not already running)
- MongoDB should be running on your system
- The system will show an error if MongoDB is not available

## 🎯 How to Use the System

1. **Open the Dashboard**: Go to http://localhost:5000
2. **Add Student Photos**: Place images in the `dataset/` folder
3. **Click "Reload Faces"**: Load the student photos
4. **Click "Start Attendance"**: Begin face recognition
5. **Students Face Camera**: Attendance marks automatically
6. **View Records**: See attendance in the list below

## 🔧 Troubleshooting

### If Python is not found:
1. Install Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your computer
4. Try again

### If MongoDB connection fails:
1. Download MongoDB from https://www.mongodb.com/try/download/community
2. Install MongoDB Community Server
3. Start MongoDB service
4. Try running the application again

### If webcam doesn't work:
1. Make sure no other app is using the webcam
2. Allow webcam access when prompted
3. Check if webcam is properly connected

### If face recognition is not accurate:
1. Use better quality photos in dataset
2. Improve lighting conditions
3. Ensure photos show the full face clearly

## 📱 Features Available

- ✅ Automatic face recognition
- ✅ Manual attendance marking
- ✅ Attendance statistics
- ✅ Date filtering
- ✅ Real-time status updates
- ✅ Duplicate prevention

## 🆘 Need Help?

1. Check the console output for error messages
2. Make sure all dependencies are installed
3. Verify MongoDB is running
4. Check webcam permissions

---

**System is ready to use!** 🎉
