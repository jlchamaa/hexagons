from fun import Fun
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pattern/<name>', methods=['GET'])
def pattern(name=None):
    f = Fun()
    if name:
        app.logger.info("{} pattern called".format(name))
        func = getattr(f, name)
        func()
    return "Pattern was {}".format(name)

app.run(host="0.0.0.0", port=8080, threaded=True)
