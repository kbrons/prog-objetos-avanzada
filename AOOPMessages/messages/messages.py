from flask import url_for
from flask import redirect
from flask import render_template
from flask import Blueprint
from flask import request
from flask_login import current_user
from AOOPMessages import db
from AOOPMessages.models import Message, User


messages = Blueprint('messages', __name__)


@messages.route('/messages', methods=['GET'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    receivedMessages = Message.query.filter_by(
        receiver_id=current_user.id
    ).all()

    users = User.query.filter(
        User.id != current_user.id
    ).all()

    return render_template('messages.html',
                           receivedMessages=receivedMessages,
                           users=users)


@messages.route('/messages', methods=['POST'])
def send_message():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    message = Message(
        author_id=current_user.id,
        receiver_id=int(request.form.get('to')),
        title=request.form.get('title'),
        body=request.form.get('body')
    )

    db.session.add(message)
    db.session.commit()

    return redirect(url_for('messages.home'))
