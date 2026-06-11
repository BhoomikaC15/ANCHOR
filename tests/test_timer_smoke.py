import unittest
from app import app, models
import time

class TimerSmokeTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app
        self.client = self.app.test_client()
        
        with app.app_context():
            models.db.create_all()
    
    def tearDown(self):
        with app.app_context():
            models.db.session.remove()
            models.db.drop_all()

    def test_timer_flow(self):
        """Test complete timer flow: start -> pause -> resume -> end"""
        with app.app_context():
            # Create user via register
            email = f'timer_test_{int(time.time())}@example.com'
            reg_resp = self.client.post('/auth/register', json={
                'username': 'tuser',
                'email': email,
                'password': 'password123'
            })
            self.assertEqual(reg_resp.status_code, 201)
            
            # Login to establish session
            login_resp = self.client.post('/auth/login', json={
                'email': email,
                'password': 'password123'
            })
            self.assertEqual(login_resp.status_code, 200)
            login_data = login_resp.get_json()
            self.assertIn('user_id', login_data)
            
            # Start timer
            start_resp = self.client.post('/timer/start')
            self.assertEqual(start_resp.status_code, 200)
            start_data = start_resp.get_json()
            self.assertIn('timer_id', start_data)
            self.assertIn('start_time', start_data)
            timer_id = start_data['timer_id']
            
            # Pause timer
            pause_resp = self.client.post('/timer/pause')
            self.assertEqual(pause_resp.status_code, 200)
            pause_data = pause_resp.get_json()
            self.assertEqual(pause_data['timer_id'], timer_id)
            self.assertIn('pause_time', pause_data)
            
            # Resume timer
            resume_resp = self.client.post('/timer/resume')
            self.assertEqual(resume_resp.status_code, 200)
            resume_data = resume_resp.get_json()
            self.assertEqual(resume_data['timer_id'], timer_id)
            self.assertIn('start_time', resume_data)
            
            # End timer
            end_resp = self.client.post('/timer/end', json={})
            self.assertEqual(end_resp.status_code, 200)
            end_data = end_resp.get_json()
            self.assertEqual(end_data['timer_id'], timer_id)
            self.assertIn('duration_seconds', end_data)
            self.assertGreaterEqual(end_data['duration_seconds'], 0)

    def test_timer_without_pause(self):
        """Test timer flow: start -> end without pause"""
        with app.app_context():
            # Create and login user
            email = f'timer_test_{int(time.time())}@example.com'
            self.client.post('/auth/register', json={
                'username': 'tuser2',
                'email': email,
                'password': 'password123'
            })
            self.client.post('/auth/login', json={
                'email': email,
                'password': 'password123'
            })
            
            # Start timer
            start_resp = self.client.post('/timer/start')
            self.assertEqual(start_resp.status_code, 200)
            timer_id = start_resp.get_json()['timer_id']
            
            # End timer directly
            end_resp = self.client.post('/timer/end', json={})
            self.assertEqual(end_resp.status_code, 200)
            end_data = end_resp.get_json()
            self.assertEqual(end_data['timer_id'], timer_id)

    def test_timer_requires_login(self):
        """Test that timer endpoints require authentication"""
        # Try to start timer without login
        start_resp = self.client.post('/timer/start')
        self.assertEqual(start_resp.status_code, 401)
        
        # Try to pause timer without login
        pause_resp = self.client.post('/timer/pause')
        self.assertEqual(pause_resp.status_code, 401)

if __name__ == '__main__':
    unittest.main()
