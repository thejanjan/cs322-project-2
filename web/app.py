"""
John Doe's Flask API.
"""

from flask import Flask, send_file, abort
import os

app = Flask(__name__, static_url_path='/pages')


@app.route("/<name>")
def fetch_page(name):
    # First, make sure the path is OK.
    filepath = f'pages/{name}'
    if not validate_path(filepath):
        abort(403)

    # Check if the file is present.
    if not os.path.isfile(filepath):
        abort(404)

    # Render the file.
    return send_file(filepath)


@app.errorhandler(403)
def error_403(e):
    return send_file('pages/403.html'), 403


@app.errorhandler(404)
def error_404(e):
    return send_file('pages/404.html'), 404


def validate_path(path: str) -> bool:
    """Returns True if the provided path is not forbidden."""
    substrings = ['..', '~']
    for substr in substrings:
        if substr in path:
            return False
    return True


if __name__ == "__main__":
    import config
    configuration = config.configuration()
    app.run(
        debug=configuration['debug'],
        host='0.0.0.0',
        port=configuration['port'],
    )
