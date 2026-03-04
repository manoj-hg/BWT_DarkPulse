from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

# Import routes
from routes.attendance import attendance_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(attendance_bp, url_prefix='/api')

# Demo faculty credentials
FACULTY_CREDENTIALS = {
    'guest': {'password': 'guest', 'name': 'Guest Faculty', 'department': 'General'},
    'faculty': {'password': 'faculty123', 'name': 'John Smith', 'department': 'Computer Science'},
    'admin': {'password': 'admin123', 'name': 'Admin User', 'department': 'Administration'}
}

@app.route('/')
def index():
    """Redirect to login page"""
    return render_template('login.html')

@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    """Handle faculty login"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Check credentials
        if username in FACULTY_CREDENTIALS:
            faculty_data = FACULTY_CREDENTIALS[username]
            if faculty_data['password'] == password:
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'faculty': {
                        'username': username,
                        'name': faculty_data['name'],
                        'department': faculty_data['department']
                    }
                })
        
        return jsonify({
            'success': False,
            'message': 'Invalid username or password'
        }), 401
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500

@app.route('/select-class')
def select_class():
    """Class selection page"""
    return render_template('select_class.html')

@app.route('/attendance')
def attendance():
    """Main attendance page"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Presidency University Attendance System is running'
    })

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('dataset', exist_ok=True)
    
    print("Starting Presidency University Face Recognition Attendance System...")
    print("Access the system at: http://localhost:5000")
    print("Default login: guest / guest")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
