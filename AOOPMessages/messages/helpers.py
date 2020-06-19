from AOOPMessages.models import User


def get_valid_user_id(rawId):
    try:
        userId = int(rawId)
        if userId < 0:
            raise ValueError

        user = User.query.filter_by(id=userId).first()
        if user is None:
            raise UserException("The user doesn't exist")

        return user.id
    except (ValueError, TypeError):
        raise UserException("The user id is not valid")


class UserException(Exception):
    pass
