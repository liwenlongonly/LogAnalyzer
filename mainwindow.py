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

class Ui_MainWindow(QtCore.QObject):

    signalUI = QtCore.pyqtSignal(str)

    isServerStarted = False

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
        self.ipLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.ipLabel.setObjectName("ipLabel")
        self.horizontalLayout.addWidget(self.ipLabel)
        self.ipLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.ipLineEdit.setEnabled(True)
        self.ipLineEdit.setPlaceholderText("ip")
        self.ipLineEdit.setObjectName("ipLineEdit")
        self.horizontalLayout.addWidget(self.ipLineEdit)
        self.portLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.portLabel.setObjectName("portLabel")
        self.horizontalLayout.addWidget(self.portLabel)
        self.portLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.portLineEdit.setObjectName("portLineEdit")
        self.horizontalLayout.addWidget(self.portLineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn.setObjectName("closebtn")
        self.horizontalLayout.addWidget(self.btn)
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

        self.queue = multiprocessing.Queue(10)

        self.retranslateUi(MainWindow)
        self.btn.clicked.connect(self.onBtnClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn.setText(_translate("MainWindow", "startServer"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.ipLabel.setText(_translate("MainWindow", "ip:"))
        self.ipLineEdit.setText(_translate("MainWindow", "127.0.0.1"))
        self.portLabel.setText(_translate("MainWindow", "port:"))
        self.portLineEdit.setText(_translate("MainWindow", "5000"))

    def onBtnClick(self):
        _translate = QtCore.QCoreApplication.translate
        if self.isServerStarted:
            self.btn.setText(_translate("MainWindow", "startServer"))
            self.process.terminate()
            self.isRuning = False
            self.queue.put("quit queue.")
        else:
            self.btn.setText(_translate("MainWindow", "closeServer"))
            self.isRuning = True
            thread = threading.Thread(target=self.readQueue)
            thread.start()
            self.process = multiprocessing.Process(target=self.worker, args=(self.queue,))
            self.process.start()
        self.isServerStarted = not self.isServerStarted

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


