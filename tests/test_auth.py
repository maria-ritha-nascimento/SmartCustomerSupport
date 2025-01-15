import unittest
from app import create_app
from app.models.database import db
from app.models.user import User

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Criar um usuário de teste
            user = User(name="Test User", email="test@example.com")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_success(self):
        response = self.client.post('/login', json={"email": "test@example.com", "password": "password"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful", response.get_json().get("message"))

    def test_login_failure(self):
        response = self.client.post('/login', json={"email": "wrong@example.com", "password": "password"})
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid email or password", response.get_json().get("error"))

    def test_protected_route_without_login(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 401)
        self.assertIn("Unauthorized access", response.get_json().get("error"))

    def test_protected_route_with_login(self):
        self.client.post('/login', json={"email": "test@example.com", "password": "password"})
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
