from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import axes3d
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class QtFigure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        # 第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # 第二步：在父类中激活Figure窗口
        super(QtFigure, self).__init__(self.fig)  # 此句必不可少，否则不能显示图形
        # 第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(1000)

    def plotSin(self):
        self.axes.grid(True)
        self.h, = self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # 构建4个随机整数，位于闭区间[0, 10]
        self.axes.cla()
        l = [np.random.randint(0, 10) for i in range(4)]
        self.axes.grid(True)
        self.axes.plot([0, 1, 2, 3], l, 'r')
        # self.h.set_ydata(l)
        self.draw()
