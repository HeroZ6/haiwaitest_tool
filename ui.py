import threading

from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton
import pyqtgraph as pg
from PySide2.QtUiTools import QUiLoader
import sys
import subprocess
import os, re, requests, json, urllib
from PySide2.QtCore import QCoreApplication, QObject, QRunnable, QThreadPool, QTimer, Qt, QCoreApplication
from pyqtgraph.Qt import QtCore
from PySide2.QtWidgets import QInputDialog, QLineEdit


class Worker(QRunnable):
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.should_stop = False

    def run(self):
        while not self.should_stop:
            # 在这里执行操作，如果要停止线程，请设置 self.should_stop 为 True，然后跳出循环
            pass


class Stats:

    def __init__(self):
        self.packname = None
        self.threadpool = None
        self.processes = None
        self.worker = None

        self.i = None
        self.x = None
        self.y = None
        self.update_timer = None
        loader = QUiLoader()
        loader.registerCustomWidget(pg.PlotWidget)
        self.ui = QUiLoader().load(r'D:\protect\haiwaitest_tool\ui\newtoolui.ui')
        self.ui.env_button.clicked.connect(self.get_device_info)
        self.ui.clear_button.clicked.connect(self.clear_result)
        self.ui.process_start.clicked.connect(self.start_plot)
        self.ui.process_clear.clicked.connect(self.clear_process)
        self.ui.stop_button.clicked.connect(self.stop_timer)
        # 提示框
        pack_name_button = QPushButton('OK')
        self.pack_name_line = QLineEdit('')
        VBoxLayout = QVBoxLayout()  # 垂直布局
        VBoxLayout.addWidget(self.pack_name_line)  # 布局的顺序与添加的顺序有关
        VBoxLayout.addWidget(pack_name_button)
        self.Dialog = QDialog()
        self.Dialog.setLayout(VBoxLayout)

    # 获取当前进程pid
    def pid_now(self):
        pid_cmd = f'adb shell ps|findstr {self.get_packname()}'
        print(pid_cmd)
        pid_content = os.popen(pid_cmd).read()
        if str(self.get_packname()) in pid_content:
            p = re.compile('      (\d.*?)   ')
            pid = p.findall(pid_content)[0]
        else:
            pid = 0
        return pid

    # 获取设备信息
    def get_device_info(self):
        try:
            ip_cmd = ['adb', 'shell', 'curl', 'ifconfig.me']
            ip_process = subprocess.Popen(ip_cmd, stdout=subprocess.PIPE)
            ip_address = ip_process.communicate()[0].decode().strip()

            info_cmd = ['adb', 'shell', 'getprop', 'ro.product.model']
            info_process = subprocess.Popen(info_cmd, stdout=subprocess.PIPE)
            device_info = info_process.communicate()[0].decode().strip()

            url = 'https://www.iplocation.net/find-ip-address'
            r = requests.session()
            r = r.get(url)
            p = re.compile('(?<=<td>)(.*?)(?=&)')
            country = p.findall(r.text)[0]
            result = f"====================环境检测结果====================\nIP：{ip_address}\n地区：{country}\n备型号：{device_info}\n=========================End========================"
            self.ui.result_label.insertPlainText(str(result))
        except Exception as e:
            print("获取检测信息失败：", e)
            self.ui.result_label.insertPlainText(str(e))
        return None, None

    # 清理开关
    # 结果栏
    def clear_result(self):
        self.ui.result_label.clear()

    # 进程栏
    def clear_process(self):
        self.ui.historyPlot.clear()

    # 获取输入的包名
    def get_packname(self):
        self.packname = self.ui.packname_input.text()
        return self.packname

    # 停止进程
    def stop_timer(self):
        self.update_timer.stop()  # 停止 QTimer

    # 关闭进程
    def closeEvent(self, event):
        # 遍历所有进程并终止它们
        for process in self.processes:
            process.terminate()

        event.accept()

    # 实时更新图

    def start_plot(self):
        if str(self.get_packname()) is None:
            self.Dialog.show()

        self.i = 0
        self.x = []
        self.y = []

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.updateData)
        self.update_timer.start(1000)  # 1000ms更新一次
        thread = threading.Thread(target=self.updateData())
        thread.start()

    def updateData(self):
        self.i += 1
        self.x.append(self.i)
        self.y.append(float(self.pid_now()))

        # 更新绘图
        self.ui.historyPlot.clear()
        self.ui.historyPlot.plot(self.x, self.y)


if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    # app.exec_()
    sys.exit(app.exec_())
