import threading
from subprocess import Popen

import qtmodern.styles
import uiautomator2 as u2
from PySide2.QtWidgets import QApplication, QMessageBox, QTextBrowser
import pyqtgraph as pg
from PySide2.QtUiTools import QUiLoader
import sys
import subprocess
import os, re, requests
from pyqtgraph.Qt import QtCore
import datetime
from aotudriver.get_info import GetInfo
from Eingpan import activiting
from PySide2.QtCore import Signal, QObject, QThread
from PySide2.QtGui import QIcon
import ctypes
from PySide2 import QtCore, QtWidgets, QtUiTools


class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    signal = Signal(object)


# 实例化
mysi = MySignals()


class Stats:

    def __init__(self):

        self.time = 0
        self.one = 0
        self.test_time = 0
        self.apppath = None
        self.old_pid = None
        self.packname = None
        self.apkpath = None
        self.tips_windows = QMessageBox()
        self.paths = ''
        self.force_stop_num = 0
        self.reset_process_num = 0
        self.i = None
        self.x = None
        self.y = None
        self.update_timer = None
        loader = QUiLoader()
        loader.registerCustomWidget(pg.PlotWidget)
        self.ui = QUiLoader().load(r'D:\protect\haiwaitest_tool\ui\main.ui')
        self.ui.setWindowTitle('haiwai_tools')
        # 初始化按钮状态
        self.ui.stop_button.setEnabled(False)
        self.ui.process_start.setEnabled(True)
        self.ui.start_time.setEnabled(True)
        self.ui.reset.setEnabled(False)
        # 按钮连接
        self.ui.env_button.clicked.connect(self.get_device_info)
        self.ui.clear_button.clicked.connect(self.clear_result)
        self.ui.process_start.clicked.connect(self.start_plot)
        self.ui.process_clear.clicked.connect(self.clear_process)
        self.ui.stop_button.clicked.connect(self.stop_timer)
        self.ui.force_stop.clicked.connect(self.force_stop)
        self.ui.uninstall_bt.clicked.connect(self.uninstall)
        self.ui.common_install.clicked.connect(self.install_apk_t)
        self.ui.debug_install.clicked.connect(self.debug_install_t)
        self.ui.auto_getpath.clicked.connect(self.get_path)
        self.ui.refresh.clicked.connect(self.get_devices)
        self.ui.start_time.clicked.connect(self.count_down_t)
        self.ui.reset.clicked.connect(self.time_reset)
        mysi.signal.connect(self.start_plot)

    def count_down_t(self):
        self.ui.start_time.setEnabled(False)
        self.ui.reset.setEnabled(True)
        self.z = 1
        self.time = self.ui.down_num.value()
        self.ui.proce_result.insertPlainText(
            f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}\n开始倒计时{self.time}秒\n')
        self.clock_timer = QtCore.QTimer()
        self.clock_timer.timeout.connect(self.count_down)
        self.clock_timer.start(1000)  # 5000ms更新一次

    def stop_timer2(self):
        self.clock_timer.stop()

    def count_down(self):
        if int(self.z) < int(self.time):
            self.ui.down_num.setValue(int(f'{int(self.time - self.z)}'))
            self.z += 1
        else:
            self.stop_timer2()
            self.ui.down_num.setValue(0)
            self.ui.proce_result.insertPlainText(
                f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}\n倒计时{self.time}秒结束\n')
            self.ui.start_time.setEnabled(True)
            self.ui.reset.setEnabled(False)

    def get_devices(self):
        cmd = 'adb shell getprop ro.product.model'
        device = os.popen(cmd).read()
        if None:
            self.ui.device_info.setText('设备未连接,或未打开usb调试')
        else:
            self.ui.device_info.setText(f'{str(device)}')

    # 截取路径
    def get_path(self):
        try:
            content = str(self.ui.result_label.toPlainText())
            p = re.compile('(?<=file:///).+')
            fpath = p.findall(content)
            self.ui.apk_path.setText(fpath[0])
            self.ui.result_label.clear()
            p1 = re.compile('_(.*?)_')
            packname = p1.findall(content)[0].replace('_', '')
            self.ui.packname_input.setText(str(packname))

        except:
            self.ui.packname_input.setText('非规范文件名,安装后获取包名')

    # 错误弹窗
    def wrong_tip(self, path):
        if str(path) == '':
            self.tips_windows.critical(
                self.ui,
                '错误',
                '路径不能为空！')
            self.stop_timer()
            return

    def print_text(self, function):
        content = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}\n==============logs=================\n{function}\n'
        self.ui.result_label.insertPlainText(content)

    def print_text2(self, function):
        content = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}\n==============logs=================\n{function}\n'
        self.ui.proce_result.insertPlainText(content)

    # 获取当前进程pid
    def pid_now(self):
        pid_cmd = f'adb shell ps|findstr {self.get_packname()}'
        pid_content = os.popen(pid_cmd).read()
        p = re.compile(self.get_packname())
        num = p.findall(pid_content)

        if str(self.get_packname()) in pid_content:
            p = re.compile('      (\d.*?)   ')
            pid = p.findall(pid_content)[0]
        else:
            pid = 0
        return pid, pid_content, num

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
            result = f"IP：{ip_address}\n地区：{country}\n备型号：{device_info}\n"
            self.print_text(result)
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
        self.ui.X_line.clear()
        self.ui.Y_line.clear()
        self.ui.time_line.clear()
        self.ui.pid_count.clear()

    def time_reset(self):
        self.stop_timer2()
        self.ui.proce_result.clear()
        self.ui.down_num.setValue(1)
        self.ui.start_time.setEnabled(True)
        self.ui.reset.setEnabled(False)

    # 获取输入的包名
    def get_packname(self):
        self.packname = self.ui.packname_input.text()
        return self.packname

    # 获取输入的apk路径
    def get_apkpath(self):
        self.apkpath = self.ui.apk_path.text()
        return self.apkpath

    # 停止进程
    def stop_timer(self):
        self.update_timer.stop()  # 停止 QTimer
        self.ui.process_start.setEnabled(True)
        self.ui.stop_button.setEnabled(False)

    def force_stop(self):
        self.force_stop_num += 1
        cmd = f'adb shell am force-stop {self.get_packname()}'
        os.popen(cmd)
        self.print_text2(f'手动强停{self.force_stop_num}次')

    def get_interval(self):
        interval = self.ui.interval.value()
        return interval

    # 实时更新图
    def start_plot(self):
        self.ui.stop_button.setEnabled(True)
        self.ui.process_start.setEnabled(False)
        self.wrong_tip(self.get_packname())
        self.i = 0
        self.x = [0]
        self.y = [0]
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.updateData)
        self.update_timer.start(int(self.get_interval()) * 1000)  # 1000ms更新一次

    def updateData(self):
        self.old_pid = self.y[-1]
        self.i += 1
        self.x.append(self.i)
        self.y.append(int(self.pid_now()[0]))
        self.last_pid = self.y[-1]
        self.ui.historyPlot.plot(self.x, self.y)
        self.ui.X_line.setText(str(self.x[-1]))
        self.ui.Y_line.setText(str(self.y[-1]))
        self.ui.time_line.setText(str(datetime.datetime.now().strftime("%H:%M:%S")))
        # 进程数
        self.ui.pid_count.setText(str(len(self.pid_now()[2])))
        thread = threading.Thread(target=self.reset_process, args=(self.last_pid, self.old_pid))
        thread.start()

    # 进程重置节点记录
    def reset_process(self, last_pid, old_pid):
        if int(self.old_pid) == 0:
            pass
        elif str(self.last_pid) != str(self.old_pid) and int(self.last_pid) != 0:
            self.reset_process_num += 1
            self.print_text2(f'进程重启{self.reset_process_num}次\n')
        else:
            pass

    # def process_window(self):

    #     # 进程结果
    #     self.ui.proce_result.insertPlainText(str(self.pid_now()[1]))

    def uninstall(self):
        self.wrong_tip(self.get_packname())
        cmd = f'adb uninstall {self.get_packname()}'
        result = os.popen(cmd)
        self.print_text(str(result.read()))

    def install_apk_t(self):
        def install_apk():
            self.wrong_tip(self.get_apkpath())
            cmd = f'adb install {self.get_apkpath()}'
            result = os.popen(cmd)
            self.print_text(str(result.read()))
            self.ui.packname_input.setText(str(GetInfo().get_appPackagename(self.apppath)))

        thread = threading.Thread(target=install_apk)
        thread.start()

    def debug_install_t(self):
        try:
            self.wrong_tip(self.get_apkpath())

            def debug_install():
                debugpath = r'D:\to'
                self.apppath = self.ui.apk_path.text()
                apppath = str(self.apppath).replace('"', '')
                get = GetInfo()
                device = u2.connect_usb(get.get_deviceids())
                acti = activiting(device)
                self.print_text(acti.install_and_debug(apppath, debugpath))
                self.ui.packname_input.setText(str(GetInfo().get_appPackagename(self.apppath)))

            thread = threading.Thread(target=debug_install)
            thread.start()
        except:
            self.ui.result_label.insertPlainText(
                f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}\n==============logs=================\n"debug安装失败,请重试"\n')


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon(r'cfg\icon.ico'))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(r"cfg\icon.png")
    stats = Stats()
    qtmodern.styles.dark(app)
    stats.ui.show()
    sys.exit(app.exec_())
