import unittest
from unittest.mock import patch
from AOOPMessages import create_app, db
from AOOPMessages.models import User, Message
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

TEST_DB = 'test.db'


class MessagesTests(unittest.TestCase):

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

            self.testUser2 = User(
                email="test2", password=generate_password_hash(
                    self.testUserPassword))

            self.testMessage = Message(
                title="test title 1",
                body="test body 1",
                timestamp=datetime.utcnow() - timedelta(days=5),
            )

            self.testMessage2 = Message(
                title="test title 2",
                body="test body 2",
                timestamp=datetime.utcnow(),
            )

        self.assertEqual(app.debug, False)

    def create_test_users(self):
        with self.app.app_context():
            db.session.add(self.testUser)
            db.session.add(self.testUser2)
            db.session.commit()

            self.testUser.id = User.query.filter_by(
                email=self.testUser.email).first().id
            self.testUser2.id = User.query.filter_by(
                email=self.testUser2.email).first().id
            self.testMessage.author_id = self.testUser.id
            self.testMessage.receiver_id = self.testUser2.id
            self.testMessage2.author_id = self.testUser2.id
            self.testMessage2.receiver_id = self.testUser.id

            db.session.add(self.testMessage)
            db.session.add(self.testMessage2)
            db.session.commit()

    @patch('flask_login.utils._get_user')
    def test_inbox(self, current_user):
        self.create_test_users()

        current_user.return_value = self.testUser

        response = self.test_client.get('/messages', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Inbox",
                      str(response.data))
        self.assertIn(self.testMessage2.title,
                      str(response.data))
        self.assertIn(self.testMessage2.body,
                      str(response.data))
        self.assertIn(self.testMessage2.timestamp.strftime('%Y-%m-%d'),
                      str(response.data))
        self.assertIn(str(self.testMessage2.author_id),
                      str(response.data))

        self.assertNotIn(self.testMessage.title,
                         str(response.data))
        self.assertNotIn(self.testMessage.body,
                         str(response.data))
        self.assertNotIn(self.testMessage.timestamp.strftime('%Y-%m-%d'),
                         str(response.data))

        current_user.return_value = self.testUser2

        response = self.test_client.get('/messages', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Inbox",
                      str(response.data))
        self.assertIn(self.testMessage.title,
                      str(response.data))
        self.assertIn(self.testMessage.body,
                      str(response.data))
        self.assertIn(self.testMessage.timestamp.strftime('%Y-%m-%d'),
                      str(response.data))
        self.assertIn(str(self.testMessage.author_id),
                      str(response.data))

        self.assertNotIn(self.testMessage2.title,
                         str(response.data))
        self.assertNotIn(self.testMessage2.body,
                         str(response.data))
        self.assertNotIn(self.testMessage2.timestamp.strftime('%Y-%m-%d'),
                         str(response.data))

    def test_inbox_not_logged_in(self):
        response = self.test_client.get('/messages', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login",
                      str(response.data))

    @patch('flask_login.utils._get_user')
    def test_send_get(self, current_user):
        self.create_test_users()

        current_user.return_value = self.testUser

        response = self.test_client.get(
            '/messages/send', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Send a message",
                      str(response.data))
        self.assertIn(self.testUser2.email,
                      str(response.data))

    def test_send_get_not_logged_in(self):
        response = self.test_client.get(
            '/messages/send', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login",
                      str(response.data))

    @patch('flask_login.utils._get_user')
    def test_send_post(self, current_user):
        self.create_test_users()

        current_user.return_value = self.testUser

        title = "test title send post"
        body = "test body send post"
        to = self.testUser2.id

        response = self.test_client.post(
            '/messages/send',
            data=dict(title=title,
                      body=body,
                      to=to
                      ),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Inbox",
                      str(response.data))

        with self.app.app_context():
            self.assertIsNotNone(Message.query.filter_by(
                receiver_id=to,
                author_id=self.testUser.id,
                title=title,
                body=body
            ).first())

    def test_send_post_not_logged_in(self):
        response = self.test_client.post(
            '/messages/send', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login",
                      str(response.data))


if __name__ == "__main__":
    unittest.main()
