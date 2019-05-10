# -*- coding: utf-8 -*-
from PyQt5 import QtCore
import numpy as np
from matplotlib.figure import Figure
import time
import matplotlib

matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class QtFigure(FigureCanvas):

    def __init__(self, width=5, height=4, dpi=100):
        # 第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # 第二步：在父类中激活Figure窗口
        super(QtFigure, self).__init__(self.fig)  # 此句必不可少，否则不能显示图形
        # 第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_figure)
        self.timer.start(1000)
        self.date_list = None

    def plot(self):
        self.axes.grid(True, linestyle='--')
        self.date_list = [0, 0, 0, 0]
        h, = self.axes.plot(self.date_list, [1, 2, 0, 4], color='r', linewidth=0.5)

    def _update_figure(self):
        # 构建4个随机整数，位于闭区间[0, 10]
        self.axes.cla()
        l = [np.random.randint(0, 10) for i in range(4)]
        self.date_list.pop(0)
        self.date_list.append(QtFigure.date_format())
        self.axes.grid(True, linestyle='--')
        self.axes.plot(self.date_list, l, color='r', linewidth=0.5)
        # self.h.set_ydata(l)
        self.draw()

    @staticmethod
    def date_format():
        return time.strftime("%H:%M:%S", time.localtime())
