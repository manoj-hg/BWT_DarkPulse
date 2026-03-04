# Presidency University Face Recognition Attendance System - Deployment Guide

## 🌐 Sharing & Deployment Options

### Option 1: Local Network Sharing (Easiest)

#### For Same WiFi Network:
1. **Find your local IP:**
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. **Start server on all interfaces:**
   ```bash
   python app.py
   ```
   The system already runs on `0.0.0.0:5000`

3. **Share this link with others:**
   ```
   http://YOUR_LOCAL_IP:5000
   ```
   Example: `http://192.168.1.100:5000`

#### Firewall Settings (if needed):
- Windows: Allow Python through Windows Firewall
- Port: 5000

### Option 2: Cloud Deployment (Professional)

#### A. PythonAnywhere (Free Tier)
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a new Web App
3. Upload your files
4. Install requirements:
   ```bash
   pip install flask opencv-python pymongo
   ```

#### B. Heroku (Free Tier)
1. Install Heroku CLI
2. Create these files:

**Procfile:**
```
web: python app.py
```

**requirements.txt:**
```
flask==2.3.3
opencv-python==4.8.1.78
pymongo==4.5.0
flask-cors==4.0.0
```

**Deploy:**
```bash
heroku create your-app-name
git add .
git commit -m "Deploy attendance system"
git push heroku main
```

#### C. Vercel (Recommended for Flask)
1. Install Vercel CLI
2. Run:
   ```bash
   vercel
   ```

### Option 3: Docker Deployment

#### Create Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

#### Build and Run:
```bash
docker build -t attendance-system .
docker run -p 5000:5000 attendance-system
```

### Option 4: Portable Distribution

#### Create executable with PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed app.py
```

#### Share the executable file with others.

## 🔧 Configuration for Sharing

### Update app.py for production:
```python
# Change this in app.py
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

### Security Considerations:
1. Change default passwords
2. Add HTTPS for production
3. Implement proper authentication
4. Add rate limiting

## 📱 Mobile Access

### Responsive Design:
- Works on tablets and phones
- Touch-friendly interface
- Adaptive layouts

### QR Code Sharing:
1. Generate QR code for your URL
2. Print and share with students
3. Students can scan and access

## 🌍 Public Deployment Steps

### For University-wide Access:

#### Step 1: Prepare Server
- Dedicated server or VPS
- Static IP address
- Domain name (optional)

#### Step 2: Server Setup
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip
pip3 install flask opencv-python pymongo

# CentOS/RHEL
sudo yum install python3 python3-pip
pip3 install flask opencv-python pymongo
```

#### Step 3: Run as Service
Create systemd service:
```bash
sudo nano /etc/systemd/system/attendance.service
```

Content:
```ini
[Unit]
Description=Presidency University Attendance System
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/your/app
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl enable attendance
sudo systemctl start attendance
```

## 🔗 Quick Sharing Links

### For Immediate Sharing:
1. **Local Network:** `http://YOUR_IP:5000`
2. **Demo Account:** guest/guest
3. **Instructions:** Share login credentials separately

### For Permanent Deployment:
1. **Choose platform:** PythonAnywhere, Heroku, or VPS
2. **Deploy using steps above**
3. **Get permanent URL**
4. **Share with stakeholders**

## 📞 Support

### For deployment issues:
1. Check firewall settings
2. Verify port 5000 is open
3. Ensure all dependencies installed
4. Test with different browsers

### For university deployment:
- Contact IT department for server access
- Request static IP if needed
- Discuss security requirements
- Plan for backup and maintenance

---

**Choose the option that best fits your needs:**
- **Quick Share:** Local network (Option 1)
- **Professional:** Cloud deployment (Option 2)
- **Enterprise:** Server deployment (Option 4)
