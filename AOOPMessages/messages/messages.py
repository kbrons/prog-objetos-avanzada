from flask import url_for
from flask import redirect
from flask import render_template
from flask import Blueprint
from flask import request
from flask import flash
from flask_login import current_user
from AOOPMessages import db
from AOOPMessages.models import Message, User
from AOOPMessages.messages.helpers import UserNotExistsError
from AOOPMessages.messages import helpers


messages = Blueprint('messages', __name__)

AUTH_LOGIN_BLUEPRINT = 'auth.login'


@messages.route('/messages', methods=['GET'])
def inbox():
    """This is the Inbox endpoint.
    Call this endpoint while logged in to read your messages

    Response codes
    --------
        - 302:
            description: The user is not logged in. Redirected to login page.
        - 200:
            description: Returns the Inbox page with all the received messages.
        - 500:
            description: There was an error retrieving the messages for the
                current user.
    """
    if not current_user.is_authenticated:
        return redirect(url_for(AUTH_LOGIN_BLUEPRINT))

    receivedMessages = Message.query.filter_by(
        receiver_id=current_user.id
    ).join(
        Message.author
    ).all()

    return render_template('messages.html',
                           receivedMessages=receivedMessages)


@messages.route('/messages/send', methods=['GET'])
def send():
    """This is the Send message form endpoint.
    Call this endpoint while logged in to fill and send a message for another
        user.

    Response codes
    --------
        - 302:
            description: The user is not logged in. Redirected to login page.
        - 200:
            description: Returns the send message form page.
        - 500:
            description: There was an error retrieving the users to send
                a message to.
    """

    if not current_user.is_authenticated:
        return redirect(url_for(AUTH_LOGIN_BLUEPRINT))

    users = User.query.filter(
        User.id != current_user.id
    ).all()

    return render_template('send_message.html',
                           users=users)


@messages.route('/messages/send', methods=['POST'])
def send_post():
    """This is the Send message endpoint.
    Call this endpoint while logged in to send a message to another user.

    Parameters
    ----------
    to : str
        Id of the user to send the message to.
    title : str
        Title of the message.
    body : str
        Body of the message.

    Response codes
    --------
        - 302:
            description: The user is not logged in. Redirected to login page.
        - 200:
            description: Sent the message and redirects to Inbox.
        - 500:
            description: There was an error sending the message.
    """

    if not current_user.is_authenticated:
        return redirect(url_for(AUTH_LOGIN_BLUEPRINT))

    try:
        receiver_id = helpers.get_valid_user_id(
            request.form.get('to'))

        message = Message(
            author_id=current_user.id,
            receiver_id=receiver_id,
            title=request.form.get('title'),
            body=request.form.get('body')
        )

        db.session.add(message)
        db.session.commit()

        return redirect(url_for('messages.inbox'))

    except UserNotExistsError as e:
        flash(message=str(e), category='error')
        return redirect(url_for('messages.send'))
