import time
import unittest

from app import app
import models


class AuthSmokeTest(unittest.TestCase):
    def test_register_and_login(self):
        email = f"auth_test_{int(time.time())}@example.com"

        with app.app_context():
            try:
                with app.test_client() as client:
                    register_response = client.post(
                        "/auth/register",
                        json={
                            "username": "auth_smoke_user",
                            "email": email,
                            "password": "secret123",
                        },
                    )
                    self.assertEqual(register_response.status_code, 201)

                    login_response = client.post(
                        "/auth/login",
                        json={"email": email, "password": "secret123"},
                    )
                    self.assertEqual(login_response.status_code, 200)
                    self.assertEqual(login_response.get_json()["username"], "auth_smoke_user")
            finally:
                models.db.session.remove()


if __name__ == "__main__":
    unittest.main()
