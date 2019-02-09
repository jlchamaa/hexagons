from fun import Fun
from flask import Flask, render_template, g
app = Flask(__name__)
f = Fun()

@app.route('/')
def index():
    def prettify(string):
        str_arr = list(string)
        need_cap = True
        for index, letter in enumerate(str_arr[:]):
            if letter == "_":
                str_arr[index] = " "
                need_cap = True
            elif need_cap:
                str_arr[index] = letter.upper()
                need_cap = False
        return ''.join(str_arr)

    patterns = [prettify(func) for func in dir(f) if not func.startswith('__')]
    patterns.sort()
    patterns.remove('Off')
    patterns.remove('Client')
    patterns.append('Off')
    g.buttons= patterns
    return render_template('index.html')

@app.route('/pattern/<name>', methods=['GET'])
def pattern(name=None):
    if name:
        name = name.replace(' ','_').lower()
        app.logger.info("{} pattern called".format(name))
        func = getattr(f, name)
        func()
    return "Pattern was {}".format(name)

portno=None
with open('portno','r') as myfile:
    portno=int(myfile.read())
app.run(host="0.0.0.0", port=portno, threaded=True)
