"""AOOPMessages main module.

This module contains the implementation of the home page.
"""

from flask import Blueprint
from flask import render_template

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    """This is the Home endpoint.
    Call this endpoint to load the home page of the website.

    Response codes
    --------
        - 200:
            description: Returns the Home page.
    """

    return render_template('index.html')
