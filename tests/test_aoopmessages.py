import unittest
from AOOPMessages import create_app, db
from AOOPMessages.models import User
from werkzeug.security import generate_password_hash


TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app = create_app(config_name='testing')
        self.app = app
        self.test_client = app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.configure(expire_on_commit=False)

            self.testUserPassword = 'test'
            self.testUser = User(
                email="test", password=generate_password_hash(
                    self.testUserPassword))

        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def create_test_user(self):
        with self.app.app_context():
            db.session.add(self.testUser)
            db.session.commit()

    def test_main_page(self):
        response = self.test_client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Advanced object oriented programming",
                      str(response.data))

    def test_404(self):
        response = self.test_client.get('/non-existent', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_successful_login(self):
        response = self.test_client.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login",
                      str(response.data))
        self.assertIn("Email",
                      str(response.data))
        self.assertIn("Password",
                      str(response.data))

        self.create_test_user()

        response = self.test_client.post(
            '/login', data=dict(email=self.testUser.email,
                                password=self.testUserPassword
                                ),
            follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Logout",
                      str(response.data))

    def test_failed_login(self):
        response = self.test_client.post(
            '/login', data=dict(email=self.testUser.email,
                                password='wrongPassword'
                                ),
            follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Please check your login details and try again...",
                      str(response.data))

        response = self.test_client.post(
            '/login', data=dict(email='wrongEmail',
                                password='wrongPassword'
                                ),
            follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Please check your login details and try again...",
                      str(response.data))

    def test_successful_logout(self):
        response = self.test_client.get(
            '/logout',
            follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Login",
                      str(response.data))

    def test_successful_signup(self):
        response = self.test_client.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sign Up",
                      str(response.data))
        self.assertIn("Email",
                      str(response.data))
        self.assertIn("Password",
                      str(response.data))

        response = self.test_client.post(
            '/signup', data=dict(email=self.testUser.email,
                                 password=self.testUserPassword
                                 ),
            follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Advanced object oriented programming",
                      str(response.data))

    def test_failed_signup(self):
        response = self.test_client.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sign Up",
                      str(response.data))
        self.assertIn("Email",
                      str(response.data))
        self.assertIn("Password",
                      str(response.data))

        self.create_test_user()

        response = self.test_client.post(
            '/signup', data=dict(email=self.testUser.email,
                                 password=self.testUserPassword
                                 ),
            follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Email address already exists...",
                      str(response.data))


if __name__ == "__main__":
    unittest.main()
