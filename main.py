import sys
import mainwindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui

class MyApplication(QApplication):
    def __init__(self, arg):
        super().__init__(arg)
        self.iconName = "home.jpeg"
        self.setWindowIcon(QtGui.QIcon(self.iconName))



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Window"
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 400
        self.iconName = "home.jpeg"


    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(self.width,self.height)



if __name__ == "__main__":
    app = MyApplication(sys.argv)
    window = MyWindow()
    window.initWindow()
    ui = mainwindow.Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())