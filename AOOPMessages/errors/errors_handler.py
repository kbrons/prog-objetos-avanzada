from flask import render_template
from flask import Blueprint


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def page_not_found(e):
    """Page not found endpoint.

    Returns a custom 404 error page.

    Parameters
    ----------
    e : Error
        The error that triggered the 404.

    Response codes
    -------
        - 404:
            description: Returns a custom not found error page.
    """

    return render_template('404.html'), 404


@errors.app_errorhandler(500)
def internal_server_error(e):
    """Internal server error endpoint.

    Returns a custom 500 error page.

    Parameters
    ----------
    e : Error
        The error that triggered the 500.

    Response codes
    -------
        - 500:
            description: Returns a custom internal error page.
    """

    return render_template('500.html'), 500
