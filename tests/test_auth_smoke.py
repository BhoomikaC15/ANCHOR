import time
import unittest

from app import app
import models


class AuthSmokeTest(unittest.TestCase):
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

    def test_register_and_login(self):
        email = f"auth_test_{int(time.time())}@example.com"

        with app.app_context():
            register_response = self.client.post(
                "/auth/register",
                json={
                    "username": "auth_smoke_user",
                    "email": email,
                    "password": "secret123",
                },
            )
            self.assertEqual(register_response.status_code, 201)

            login_response = self.client.post(
                "/auth/login",
                json={"email": email, "password": "secret123"},
            )
            self.assertEqual(login_response.status_code, 200)
            self.assertEqual(login_response.get_json()["username"], "auth_smoke_user")


if __name__ == "__main__":
    unittest.main()
