// Global variables
let isAttendanceRunning = false;
let currentStatus = null;
let TOTAL_STUDENTS = 60; // Will be updated based on selected class

// Load faculty and class info
function loadFacultyInfo() {
    const session = localStorage.getItem('faculty_session');
    if (session) {
        const faculty = JSON.parse(session);
        document.getElementById('faculty-avatar').textContent = faculty.name.charAt(0).toUpperCase();
    } else {
        window.location.href = '/login';
    }
}

function loadClassInfo() {
    const selectedClass = localStorage.getItem('selected_class');
    if (selectedClass) {
        const classInfo = JSON.parse(selectedClass);
        document.getElementById('class-name').textContent = classInfo.name;
        document.getElementById('class-details').textContent = `${classInfo.section} - ${classInfo.semester}`;
        document.getElementById('strength-number').textContent = classInfo.strength;
        document.getElementById('class-info').textContent = `${classInfo.name} - ${classInfo.section}`;
        TOTAL_STUDENTS = classInfo.strength;
        
        // Reset attendance stats
        updateAttendanceStats(0);
    } else {
        window.location.href = '/select-class';
    }
}

// Logout function
function logout() {
    localStorage.removeItem('faculty_session');
    localStorage.removeItem('selected_class');
    window.location.href = '/login';
}

// Go to class selection
function goToClassSelection() {
    window.location.href = '/select-class';
}

// Page Navigation
function showPage(pageName) {
    // Hide all pages
    document.getElementById('attendance-page').style.display = 'none';
    document.getElementById('dashboard-page').style.display = 'none';
    
    // Show selected page
    document.getElementById(`${pageName}-page`).style.display = 'block';
    
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Load data for the page
    if (pageName === 'dashboard') {
        loadAttendance();
    }
}

// Update time and date
function updateDateTime() {
    const now = new Date();
    
    // Update time
    const timeString = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });
    document.getElementById('current-time').textContent = timeString;
    
    // Update date
    const dateString = now.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    document.getElementById('current-date').textContent = dateString;
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    loadFacultyInfo();
    loadClassInfo();
    
    // Update time immediately and then every second
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    checkSystemStatus();
    loadAttendance();
    loadStats();
    loadPresentStudents();
    loadRegisteredStudents();
    
    // Set today's date as default in date filter
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date-filter').value = today;
    
    // Auto-refresh status every 5 seconds
    setInterval(checkSystemStatus, 5000);
    
    // Auto-refresh attendance and present students every 10 seconds
    setInterval(loadAttendance, 10000);
    setInterval(loadStats, 10000);
    setInterval(loadPresentStudents, 10000);
    
    // Refresh registered students every 30 seconds (less frequent)
    setInterval(loadRegisteredStudents, 30000);
});

// Show loading overlay
function showLoading() {
    document.getElementById('loading-overlay').classList.remove('hidden');
}

// Hide loading overlay
function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

// Show message in specified element
function showMessage(elementId, message, type = 'info') {
    const messageElement = document.getElementById(elementId);
    messageElement.textContent = message;
    messageElement.className = `message ${type}`;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageElement.textContent = '';
        messageElement.className = 'message';
    }, 5000);
}

// Check system status
async function checkSystemStatus() {
    try {
        const response = await fetch('/api/recognition-status');
        const data = await response.json();
        
        if (data.success) {
            updateSystemStatus(data.status);
            currentStatus = data.status;
        } else {
            console.error('Failed to get status:', data.message);
        }
    } catch (error) {
        console.error('Error checking status:', error);
        updateSystemStatus({ is_running: false, known_faces_count: 0 });
    }
}

// Update system status display
function updateSystemStatus(status) {
    const indicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const knownFacesElement = document.getElementById('known-faces');
    
    if (status.is_running) {
        indicator.className = 'status-indicator active';
        statusText.textContent = 'Face Recognition Running';
        startBtn.disabled = true;
        stopBtn.disabled = false;
        isAttendanceRunning = true;
    } else {
        indicator.className = 'status-indicator inactive';
        statusText.textContent = 'Face Recognition Stopped';
        startBtn.disabled = false;
        stopBtn.disabled = true;
        isAttendanceRunning = false;
    }
    
    knownFacesElement.textContent = status.known_faces_count || 0;
}

// Start attendance
async function startAttendance() {
    showLoading();
    
    try {
        const response = await fetch('/api/start-attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('control-message', data.message, 'success');
            // Update status immediately
            setTimeout(checkSystemStatus, 1000);
            loadStats();
        } else {
            showMessage('control-message', data.message, 'error');
        }
    } catch (error) {
        console.error('Error starting attendance:', error);
        showMessage('control-message', 'Failed to start attendance', 'error');
    } finally {
        hideLoading();
    }
}

// Stop attendance
async function stopAttendance() {
    showLoading();
    
    try {
        const response = await fetch('/api/stop-attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('control-message', data.message, 'success');
            // Update status immediately
            setTimeout(checkSystemStatus, 1000);
        } else {
            showMessage('control-message', data.message, 'error');
        }
    } catch (error) {
        console.error('Error stopping attendance:', error);
        showMessage('control-message', 'Failed to stop attendance', 'error');
    } finally {
        hideLoading();
    }
}

// Reload faces
async function reloadFaces() {
    showLoading();
    
    try {
        const response = await fetch('/api/reload-faces', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('control-message', data.message, 'success');
            document.getElementById('known-faces').textContent = data.faces_count;
            loadStats();
        } else {
            showMessage('control-message', data.message, 'error');
        }
    } catch (error) {
        console.error('Error reloading faces:', error);
        showMessage('control-message', 'Failed to reload faces', 'error');
    } finally {
        hideLoading();
    }
}

// Mark manual attendance
async function markManualAttendance() {
    const studentName = document.getElementById('student-name').value.trim();
    
    if (!studentName) {
        showMessage('manual-message', 'Please enter a student name', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/mark-manual', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_name: studentName
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('manual-message', data.message, 'success');
            document.getElementById('student-name').value = '';
            loadAttendance();
            loadStats();
            loadPresentStudents();
        } else {
            showMessage('manual-message', data.message, 'error');
        }
    } catch (error) {
        console.error('Error marking manual attendance:', error);
        showMessage('manual-message', 'Failed to mark attendance', 'error');
    } finally {
        hideLoading();
    }
}

// Register new student
async function registerNewStudent() {
    const studentName = document.getElementById('new-student-name').value.trim();
    
    if (!studentName) {
        showMessage('registration-message', 'Please enter a student name', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/register-student', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_name: studentName
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('registration-message', data.message, 'success');
            document.getElementById('new-student-name').value = '';
            loadRegisteredStudents();
            loadStats(); // Update known faces count
        } else {
            showMessage('registration-message', data.message, 'error');
        }
    } catch (error) {
        console.error('Error registering student:', error);
        showMessage('registration-message', 'Failed to register student', 'error');
    } finally {
        hideLoading();
    }
}

// Load registered students
async function loadRegisteredStudents() {
    try {
        const response = await fetch('/api/registered-students');
        const data = await response.json();
        
        if (data.success) {
            displayRegisteredStudents(data.students);
            document.getElementById('registered-count').textContent = data.count;
        } else {
            console.error('Failed to load registered students:', data.message);
            displayRegisteredStudents([]);
        }
    } catch (error) {
        console.error('Error loading registered students:', error);
        displayRegisteredStudents([]);
    }
}

// Display registered students
function displayRegisteredStudents(students) {
    const listElement = document.getElementById('registered-list');
    
    if (students.length === 0) {
        listElement.innerHTML = '<p>No registered students found</p>';
        return;
    }
    
    const html = students.map(student => `
        <div class="student-item">
            <span class="student-name">${student}</span>
        </div>
    `).join('');
    
    listElement.innerHTML = html;
}

// Load present students
async function loadPresentStudents() {
    try {
        const response = await fetch('/api/present-students');
        const data = await response.json();
        
        if (data.success) {
            displayPresentStudents(data.present_students);
            document.getElementById('present-count').textContent = data.count;
        } else {
            console.error('Failed to load present students:', data.message);
            displayPresentStudents([]);
        }
    } catch (error) {
        console.error('Error loading present students:', error);
        displayPresentStudents([]);
    }
}

// Display present students
function displayPresentStudents(presentStudents) {
    const listElement = document.getElementById('present-students');
    
    if (presentStudents.length === 0) {
        listElement.innerHTML = '<p class="empty-state">No students marked present yet</p>';
        updateAttendanceStats(0);
        return;
    }
    
    const html = presentStudents.map(student => 
        `<span class="present-student">${student}</span>`
    ).join('');
    
    listElement.innerHTML = html;
    updateAttendanceStats(presentStudents.length);
}

// Update attendance statistics
function updateAttendanceStats(presentCount) {
    const absentCount = TOTAL_STUDENTS - presentCount;
    const percentage = Math.round((presentCount / TOTAL_STUDENTS) * 100);
    
    document.getElementById('present-count').textContent = presentCount;
    document.getElementById('absent-count').textContent = absentCount;
    document.getElementById('attendance-percentage').textContent = `${percentage}%`;
}

// Load attendance records
async function loadAttendance() {
    try {
        const dateFilter = document.getElementById('date-filter').value;
        let url = '/api/attendance-list';
        
        if (dateFilter) {
            url += `?date=${dateFilter}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            displayAttendanceList(data.data);
        } else {
            console.error('Failed to load attendance:', data.message);
            displayAttendanceList([]);
        }
    } catch (error) {
        console.error('Error loading attendance:', error);
        displayAttendanceList([]);
    }
}

// Display attendance list
function displayAttendanceList(attendanceRecords) {
    const listElement = document.getElementById('attendance-list');
    
    if (attendanceRecords.length === 0) {
        listElement.innerHTML = '<p>No attendance records found</p>';
        return;
    }
    
    const html = attendanceRecords.map(record => `
        <div class="attendance-item">
            <span class="student-name">${record.student_name}</span>
            <div class="attendance-info">
                <span>📅 ${record.date}</span>
                <span>🕐 ${record.time}</span>
            </div>
        </div>
    `).join('');
    
    listElement.innerHTML = html;
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/attendance-stats');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('today-count').textContent = data.stats.today_attendance;
            document.getElementById('total-students').textContent = data.stats.total_unique_students;
        } else {
            console.error('Failed to load stats:', data.message);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Clear date filter
function clearDateFilter() {
    document.getElementById('date-filter').value = '';
    loadAttendance();
}

// Clear all records
async function clearAllRecords() {
    if (!confirm('Are you sure you want to delete ALL attendance records? This action cannot be undone.')) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/clear-all-records', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('control-message', data.message, 'success');
            loadAttendance();
            loadStats();
            loadPresentStudents();
        } else {
            showMessage('control-message', data.message, 'error');
        }
    } catch (error) {
        console.error('Error clearing all records:', error);
        showMessage('control-message', 'Failed to clear all records', 'error');
    } finally {
        hideLoading();
    }
}

// Clear old records
async function clearOldRecords() {
    if (!confirm('Are you sure you want to delete attendance records older than 30 days? This action cannot be undone.')) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/clear-old-records', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                days: 30
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('control-message', data.message, 'success');
            loadAttendance();
            loadStats();
            loadPresentStudents();
        } else {
            showMessage('control-message', data.message, 'error');
        }
    } catch (error) {
        console.error('Error clearing old records:', error);
        showMessage('control-message', 'Failed to clear old records', 'error');
    } finally {
        hideLoading();
    }
}

// Handle Enter key in input fields
document.addEventListener('DOMContentLoaded', function() {
    const studentNameInput = document.getElementById('student-name');
    const newStudentNameInput = document.getElementById('new-student-name');
    
    if (studentNameInput) {
        studentNameInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                markManualAttendance();
            }
        });
    }
    
    if (newStudentNameInput) {
        newStudentNameInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                registerNewStudent();
            }
        });
    }
});

// Utility function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Utility function to format time
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}
