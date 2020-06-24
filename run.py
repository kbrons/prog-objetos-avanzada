"""Run module.

This module creates and runs the Flask app with the default parameters
and settings.
"""

from AOOPMessages import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
