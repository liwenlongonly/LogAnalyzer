# -*- coding: utf-8 -*-
from flask import Flask, request


flask = Flask(__name__)
flask.msg_queue = None


@flask.route('/', methods=['GET'])
def _index():
    return "<h1>hello world!</h1>"


@flask.route('/ssrc', methods=['GET'])
def _ssrc_get():
    if not flask.msg_queue.full():
        r = request.args.get('info')
        if r is not None:
            _put_queue("hello world!")
        else:
            _put_queue(r)
        return '{"code":200}'
    else:
        return '{"code":300,"msg":"queue is full"}'


@flask.route('/ssrc', methods=['POST'])
def _ssrc_post():
    if not flask.msg_queue.full():
        r = request.form.get("info", default='hello world!')
        _put_queue(r)
        return '{"code":200}'
    else:
        return '{"code":300,"msg":"queue is full"}'


def _put_queue(msg):
    if not flask.msg_queue.full():
        flask.msg_queue.put(msg)


if __name__ == '__main__':
    flask.run(debug=False, threaded=True)
