# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qthello.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from httpserver import app
import multiprocessing
import threading
import socket
import re
from qtfigure import QtFigure

class Ui_MainWindow(QtCore.QObject):

    signalUI = QtCore.pyqtSignal(str)

    isServerStarted = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.gridlayout = QtWidgets.QGridLayout(self.centralwidget)  # 继承容器groupBox
        self.figure = QtFigure(width=3, height=2, dpi=100)
        self.figure.plotSin()
        self.gridlayout.addWidget(self.figure)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(90, 10, 431, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ipLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.ipLabel.setObjectName("ipLabel")
        self.horizontalLayout.addWidget(self.ipLabel)
        self.ipLineEdit = QtWidgets.QLineEdit()
        self.ipLineEdit.setPlaceholderText("ip")
        self.ipLineEdit.setObjectName("ipLineEdit")
        self.horizontalLayout.addWidget(self.ipLineEdit, stretch=7)
        self.portLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.portLabel.setObjectName("portLabel")
        self.horizontalLayout.addWidget(self.portLabel)
        self.portLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.portLineEdit.setObjectName("portLineEdit")
        self.portLineEdit.setEnabled(True)
        self.horizontalLayout.addWidget(self.portLineEdit, stretch=2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn.setObjectName("closebtn")
        self.horizontalLayout.addWidget(self.btn)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.signalUI.connect(self.showMessage)
        self.queue = multiprocessing.Queue(10)
        self.btn.clicked.connect(self.onBtnClick)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.btn.setText(_translate("MainWindow", "startServer"))
        self.ipLabel.setText(_translate("MainWindow", "ip:"))
        addrs = self.getHostIp()
        self.ipLineEdit.setText(_translate("MainWindow", addrs))
        self.portLabel.setText(_translate("MainWindow", "port:"))
        self.portLineEdit.setText(_translate("MainWindow", "5000"))


    def onBtnClick(self):
        _translate = QtCore.QCoreApplication.translate
        if self.isServerStarted:
            self.process.terminate()
            self.isRuning = False
            self.queue.put("quit queue.")
            self.btn.setText(_translate("MainWindow", "startServer"))
        else:
            ip = self.ipLineEdit.text()
            if not self.checkIp(ip):
                self.signalUI.emit("ip is not match.")
                return
            port = self.portLineEdit.text()
            if not port.isnumeric():
                return
            self.isRuning = True
            thread = threading.Thread(target=self.readQueue)
            thread.start()
            self.process = multiprocessing.Process(target=self.worker, args=(self.queue, ip, port))
            self.process.start()
            self.btn.setText(_translate("MainWindow", "closeServer"))
        self.isServerStarted = not self.isServerStarted


    def worker(self, q, host, port):
        app.queue = q
        app.run(host=host, port=int(port), debug=False, threaded=True)


    def readQueue(self):
        while True:
            if self.isRuning:
               data = self.queue.get(block=True)
               print(data)
               self.signalUI.emit(data)
            else:
                break


    def showMessage(self, str):
        self.statusbar.showMessage(str)


    def checkIp(self, ipAddr):
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if compile_ip.match(ipAddr):
            return True
        else:
            return False


    def getHostIp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

