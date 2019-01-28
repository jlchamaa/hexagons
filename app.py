from fun import Fun
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    f = Fun()
    f.pumpkin()
    return 'Jenn, World!'
