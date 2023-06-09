import os
import re
from PySide2 import QtWidgets
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg

from random import randint
from PySide2.QtGui import QColor


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('pyqtgraph作图')

        # 创建 PlotWidget 对象
        self.pw = pg.PlotWidget()

        # 设置图表标题
        self.pw.setTitle("实时进程",
                         color=QColor("#008080"),
                         size='12pt')

        # 设置上下左右的label
        self.pw.setLabel("left", "进程")
        self.pw.setLabel("bottom", "时间")

        # # 设置X轴 刻度 范围
        self.pw.setYRange(min=0,  # 最小值
                          max=300)  # 最大值

        # 显示表格线
        self.pw.showGrid(x=True, y=True)

        # 背景色改为白色
        self.pw.setBackground('w')

        # 设置Y轴 刻度 范围
        self.pw.setYRange(min=0,  # 最小值
                          max=99999)  # 最大值

        # 居中显示 PlotWidget
        self.setCentralWidget(self.pw)

        # 实时显示应该获取 PlotDataItem对象, 调用其setData方法，
        # 这样只重新plot该曲线，性能更高
        self.curve = self.pw.plot(
            pen=pg.mkPen('r', width=1)
        )

        self.i = 0
        self.x = []  # x轴的值
        self.y = []  # y轴的值

        # 启动定时器，每隔1秒通知刷新一次数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateData)
        self.timer.start(1000)

    def updateData(self):
        self.i += 1
        self.x.append(self.i)
        # 创建随机温度值
        self.y.append(int(self.pid_now(packname)))

        # plot data: x, y values
        self.curve.setData(self.x, self.y)

    def pid_now(self, packname):
        pid_cmd = f'adb shell ps|findstr {packname}'
        pid_content = os.popen(pid_cmd).read()
        if packname in pid_content:
            p = re.compile('      (\d.*?)   ')
            pid = p.findall(pid_content)[0]
        else:
            pid = 1
        return pid


if __name__ == '__main__':
    packname = 'com.android.yctswzu.tsdctsking'
    app = QtWidgets.QApplication()
    main = MainWindow()
    main.show()
    app.exec_()

