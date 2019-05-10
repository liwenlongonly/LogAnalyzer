# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from main_window import MyMainWindow


class MyApplication(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.setWindowIcon(QtGui.QIcon("home.jpeg"))


if __name__ == "__main__":
    app = MyApplication(sys.argv)
    window = MyMainWindow()
    window.init_window()
    window.show()
    sys.exit(app.exec_())
