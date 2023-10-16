"""
John Doe's Flask API.
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "UOCIS docker demo!\n"

if __name__ == "__main__":
    import config
    configuration = config.configuration()
    app.run(
        debug=configuration['debug'],
        host='0.0.0.0',
        port=configuration['port'],
    )
