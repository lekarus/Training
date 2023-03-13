from flask import Flask

app = Flask(__name__)

from db import db

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
