# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qthello.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtCore
from httpserver import app
import multiprocessing
import threading

class Ui_MainWindow(QtCore.QObject):

    signalUI = QtCore.pyqtSignal(str)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(606, 402)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(90, 10, 431, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startbtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.startbtn.setObjectName("startbtn")
        self.horizontalLayout.addWidget(self.startbtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closebtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.closebtn.setObjectName("closebtn")
        self.horizontalLayout.addWidget(self.closebtn)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(69, 95, 481, 121))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 606, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.signalUI.connect(self.setLabelText)

        self.retranslateUi(MainWindow)
        self.closebtn.clicked.connect(self.closeServer)
        self.startbtn.clicked.connect(self.startServer)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def startServer(self):
        self.isRuning = True
        self.queue = multiprocessing.Queue(10)
        thread = threading.Thread(target=self.readQueue)
        thread.start()
        self.process = multiprocessing.Process(target=self.worker, args=(self.queue,))
        self.process.start()

    def closeServer(self):
        self.process.terminate()
        self.isRuning = False
        self.queue.put("quit queue.")

    def worker(self, q):
        app.queue = q
        app.run(debug=False, threaded=True)

    def readQueue(self):
        while True:
            if self.isRuning:
               data = self.queue.get(block=True)
               print(data)
               self.signalUI.emit(data)
            else:
                break

    def setLabelText(self, str):
        self.label.setText("{}\n{}".format(self.label.text(), str))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startbtn.setText(_translate("MainWindow", "startServer"))
        self.closebtn.setText(_translate("MainWindow", "closeServer"))
        self.label.setText(_translate("MainWindow", "TextLabel"))


