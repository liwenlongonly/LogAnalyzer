import sys
import mainwindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Window"
        self.top = 10
        self.left = 10
        self.width = 400
        self.height = 300
        self.iconName = "home.jpeg"


    def initWindow(self):
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.initWindow()
    ui = mainwindow.Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())