from fun import Fun
from multiprocessing import Process, Queue
from flask import Flask, render_template, g, request
app = Flask(__name__)
q = Queue()
f= Fun()
p = Process(target=f._run, args=(q,))
p.start()

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

    patterns = [prettify(func) for func in dir(f) if not func.startswith('_')]
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
        q.put(name)
    return "Pattern was {}".format(name)

@app.route('/custom',methods=['GET'])
def custom():
    return render_template('custom.html')

@app.route('/apply', methods=['POST'])
def apply():
    f.client.put_pixels(request.json)
    return "Success", 200


portno=None
with open('portno','r') as myfile:
    portno=int(myfile.read())
app.run(host="0.0.0.0", port=portno, threaded=True)
