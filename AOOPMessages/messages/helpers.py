from AOOPMessages.models import User


def get_valid_user_id(rawId):
    """Get Valid User Id

    This method validates the received id and makes sure it belongs to
    an existing user.


    Parameters
    ----------
    rawId : string
        User id to validate.

    Returns
    -------
    int
        The validated user id.

    Raises
    ------
    TypeError
        If the received id can't be parsed to an int
    ValueError
        If the received id isn't valid
    UserNotExistsError
        If the user doesn't exist in the database

    """

    try:
        userId = int(rawId)
        if userId < 0:
            raise ValueError

        user = User.query.filter_by(id=userId).first()
        if user is None:
            raise UserNotExistsError("The user doesn't exist")

        return user.id
    except (ValueError, TypeError):
        raise UserNotExistsError("The user id is not valid")


class UserNotExistsError(Exception):
    """UserNotExistsError

    This error should be raised when trying to operate with a user id
    that doesn't exist in the database.
    """
    pass
