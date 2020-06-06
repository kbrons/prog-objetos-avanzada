from flask import url_for
from flask import redirect
from flask import render_template
from flask import Blueprint
from flask_login import current_user
from AOOPMessages.models import User, Message


messages = Blueprint('messages', __name__)


@messages.route('/', methods=['GET'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    receivedMessages = Message.query.filter_by(
        receiver_id=current_user.id
    ).all()

    authorIds = map(lambda message: message.author_id, receivedMessages)

    authors = User.query.filter_by(User.id.in_(authorIds)).with_entities(
        User.id, User.email).all()

    authorDict = {}
    for author in authors:
        authorDict[author.id] = author.email

    return render_template('received_messages.html',
                           receivedMessages=receivedMessages,
                           authors=authorDict)
