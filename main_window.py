# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtCore
from qt_figure import QtFigure
from http_server import flask
import socket
import multiprocessing
import threading
import re


class MyPushButton(QtWidgets.QPushButton):
    is_clicked = False


class MyMainWindow(QMainWindow):

    ui_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.title = "Log Analyzer"
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 400
        self.push_btn = None
        self.ip_line_edit = None
        self.port_label_edit = None
        self.status_bar = None
        self.msg_queue = multiprocessing.Queue(10)
        self.process = None
        self.read_queue_is_runing = False

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(self.width, self.height)

        centralist = QtWidgets.QWidget()
        self.setCentralWidget(centralist)

        grid_layout = QtWidgets.QGridLayout(centralist)  # 继承容器groupBox
        figure = QtFigure(width=3, height=2, dpi=100)
        figure.plot()
        grid_layout.addWidget(figure)

        horizontally_widget = QtWidgets.QWidget(centralist)
        horizontally_widget.setGeometry(QtCore.QRect(90, 10, 431, 41))

        horizontal_layout = QtWidgets.QHBoxLayout(horizontally_widget)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        ip_label = QtWidgets.QLabel(horizontally_widget)
        ip_label.setText("ip")
        horizontal_layout.addWidget(ip_label)

        self.ip_line_edit = QtWidgets.QLineEdit()
        self.ip_line_edit.setPlaceholderText("ip")
        horizontal_layout.addWidget(self.ip_line_edit, stretch=7)

        port_label = QtWidgets.QLabel(horizontally_widget)
        port_label.setText("port")
        horizontal_layout.addWidget(port_label)

        self.port_label_edit = QtWidgets.QLineEdit(horizontally_widget)
        self.port_label_edit.setEnabled(True)

        horizontal_layout.addWidget(self.port_label_edit, stretch=2)
        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontal_layout.addItem(spacer_item)

        self.push_btn = MyPushButton(horizontally_widget)
        self.push_btn.clicked.connect(lambda: self._on_btn_click(self.push_btn))
        horizontal_layout.addWidget(self.push_btn)

        menu_bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(menu_bar)

        self.status_bar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.ui_signal.connect(self._show_message)

        self._default_config()

    def _default_config(self):
        self.push_btn.setText("startServer")
        addr = MyMainWindow.get_host_ip()
        self.ip_line_edit.setText(addr)
        self.port_label_edit.setText("5000")

    def _on_btn_click(self, sender):
        if sender.is_clicked:
            self.process.terminate()
            self.read_queue_is_runing = False
            self.msg_queue.put("quit queue.")
            sender.setText("startServer")
        else:
            ip = self.ip_line_edit.text()
            if not self.check_ip(ip):
                self.ui_signal.emit("ip is not match.")
                return
            port = self.port_label_edit.text()
            if not port.isnumeric():
                return
            self.read_queue_is_runing = True
            thread = threading.Thread(target=self._read_queue)
            thread.start()
            self.process = multiprocessing.Process(target=self._worker, args=(self.msg_queue, ip, port))
            self.process.start()
            sender.setText("closeServer")
        sender.is_clicked = not sender.is_clicked

    def _show_message(self, msg):
        self.status_bar.showMessage(msg)

    def _read_queue(self):
        while True:
            if self.read_queue_is_runing:
                data = self.msg_queue.get(block=True)
                print(data)
                self.ui_signal.emit(data)
            else:
                break

    def _worker(self, q, host, port):
        flask.msg_queue = q
        # ssl_context = ("cert/cert.pem", "cert/key.pem")
        flask.run(host=host, port=int(port), debug=False, threaded=True)

    @staticmethod
    def check_ip(ip):
        compile_ip = re.compile(
            "^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$")
        if compile_ip.match(ip):
            return True
        else:
            return False

    @staticmethod
    def get_host_ip():
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        if ip is None:
            ip = "127.0.0.1"
        return ip
