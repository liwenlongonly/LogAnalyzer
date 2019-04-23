from flask import Flask, request
app = Flask(__name__)

app.queue = None

@app.route('/ssrc', methods=['GET'])
def get():
    if not app.queue.full():
        r = request.args.get('info')
        if r == None:
            putQueue("hello world!")
        else:
            putQueue(r)
        return '{"code":200}'
    else:
        return '{"code":300,"msg":"queue is full"}'

@app.route('/ssrc', methods=['POST'])
def post():
    if not app.queue.full():
        r = request.form.get("info", default='hello world!')
        putQueue(r)
        return '{"code":200}'
    else:
        return '{"code":300,"msg":"queue is full"}'

def putQueue(str):
    if not app.queue.full():
        app.queue.put(str)

if __name__ == '__main__':
  app.run(debug=False, threaded=True)