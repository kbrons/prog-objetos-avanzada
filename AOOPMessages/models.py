"""AOOPMessages models module.

This module contains the classes representing the application model.
"""

from AOOPMessages import db
from AOOPMessages import login_manager
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    """Load User for Login Manager implementation.

    Method to retrieve the current_user for the Login Manager module.

    Parameters
    ----------
        user_id : int
            Id of the logged in user.

    Returns
    -------
        User
            User instance of the logged in user.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """

    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User class.

    Class defining the user model for the application.

    Attributes
    ----------
        id : int
            Id of the user.
        email : str
            Email of the user.
        password : str
            Hashed password of the user.

    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return f"<User {self.id}>"


class Message(db.Model):
    """Message class.

    Class defining the message model for the application.

    Attributes
    ----------
        id : int
            Id of the message.
        title : str
            Title of the message.
        Body : str
            Body of the message.
        timestamp : DateTime
            Date and time when the message was sent.
        author_id : int
            Id of the user that sent the message.
        receiver_id : int
            Id of the user that received the message.
        author : User
            User that sent the message.
        receiver : User
            User that received the message.

    """

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("User", foreign_keys=[author_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
