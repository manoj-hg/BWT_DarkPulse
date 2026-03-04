from pymongo import MongoClient
from datetime import datetime, date
import os

class AttendanceModel:
    """MongoDB model for attendance records"""
    
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['attendance_db']
        self.collection = self.db['attendance']
        
    def mark_attendance(self, student_name):
        """
        Mark attendance for a student
        Prevents duplicate entries for the same day
        """
        try:
            today = date.today().isoformat()
            
            # Check if attendance already marked today
            existing_record = self.collection.find_one({
                'student_name': student_name,
                'date': today
            })
            
            if existing_record:
                return {
                    'success': False,
                    'message': f'Attendance already marked for {student_name} today'
                }
            
            # Create new attendance record
            attendance_record = {
                'student_name': student_name,
                'date': today,
                'time': datetime.now().strftime('%H:%M:%S'),
                'timestamp': datetime.now(),
                'created_at': datetime.now().isoformat()
            }
            
            # Insert into database
            result = self.collection.insert_one(attendance_record)
            
            return {
                'success': True,
                'message': f'Attendance marked for {student_name}',
                'record_id': str(result.inserted_id),
                'data': {
                    'student_name': student_name,
                    'date': today,
                    'time': attendance_record['time']
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def get_attendance_list(self, date_filter=None):
        """
        Get list of attendance records
        Optional date filter to get records for specific date
        """
        try:
            query = {}
            if date_filter:
                query['date'] = date_filter
            
            # Get records sorted by timestamp (newest first)
            records = list(self.collection.find(query).sort('timestamp', -1))
            
            # Convert ObjectId to string and format records
            formatted_records = []
            for record in records:
                formatted_records.append({
                    'id': str(record['_id']),
                    'student_name': record['student_name'],
                    'date': record['date'],
                    'time': record['time'],
                    'timestamp': record['created_at']
                })
            
            return {
                'success': True,
                'data': formatted_records,
                'count': len(formatted_records)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}',
                'data': []
            }
    
    def get_attendance_stats(self):
        """Get attendance statistics"""
        try:
            # Get today's attendance
            today = date.today().isoformat()
            today_records = list(self.collection.find({'date': today}))
            
            # Get total unique students
            unique_students = self.collection.distinct('student_name')
            
            # Get attendance for last 7 days
            from datetime import timedelta
            week_ago = (date.today() - timedelta(days=7)).isoformat()
            week_records = list(self.collection.find({'date': {'$gte': week_ago}}))
            
            return {
                'success': True,
                'stats': {
                    'today_attendance': len(today_records),
                    'total_unique_students': len(unique_students),
                    'week_attendance': len(week_records)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Stats error: {str(e)}'
            }
    
    def clear_all_records(self):
        """Clear ALL attendance records from database"""
        try:
            result = self.collection.delete_many({})
            
            return {
                'success': True,
                'message': f'Deleted all {result.deleted_count} records'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Delete error: {str(e)}'
            }
    
    def clear_old_records(self, days=30):
        """Clear attendance records older than specified days"""
        try:
            from datetime import timedelta
            cutoff_date = (date.today() - timedelta(days=days)).isoformat()
            
            result = self.collection.delete_many({
                'date': {'$lt': cutoff_date}
            })
            
            return {
                'success': True,
                'message': f'Deleted {result.deleted_count} old records'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Delete error: {str(e)}'
            }
