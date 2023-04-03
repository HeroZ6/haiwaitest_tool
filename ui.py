import threading
import time
import uiautomator2 as u2
from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QMessageBox
import pyqtgraph as pg
from PySide2.QtUiTools import QUiLoader
import sys
import subprocess
import os, re, requests
from pyqtgraph.Qt import QtCore
from PySide2.QtWidgets import QLineEdit
import datetime
from aotudriver.get_info import GetInfo
from Eingpan import activiting


class Stats:

    def __init__(self):
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
        self.ui = QUiLoader().load(r'D:\protect\haiwaitest_tool\ui\newtoolui.ui')
        self.ui.env_button.clicked.connect(self.get_device_info)
        self.ui.clear_button.clicked.connect(self.clear_result)
        self.ui.process_start.clicked.connect(self.start_plot)
        self.ui.process_clear.clicked.connect(self.clear_process)
        self.ui.stop_button.clicked.connect(self.stop_timer)
        self.ui.force_stop.clicked.connect(self.force_stop)
        self.ui.uninstall_bt.clicked.connect(self.uninstall)
        self.ui.common_install.clicked.connect(self.install_apk)
        self.ui.debug_install.clicked.connect(self.debug_install_t)


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

    # 获取输入的包名
    def get_packname(self):
        self.packname = self.ui.packname_input.text()
        return self.packname

    # 获取输入的apk路径
    def get_apkpath(self):
        self.apkpath = self.ui.apk_path.text()
        return self.apkpath
    # def get_filepath(self):
    #     content = self.ui.result_label.text()
    #     p = re.compile('file:///.*')
    #     file_path = p.findall(content)
    #     self.ui.apk_path.setText(str(file_path))
    #     print(file_path)
    # 停止进程
    def stop_timer(self):
        self.update_timer.stop()  # 停止 QTimer

    def force_stop(self):
        self.force_stop_num += 1
        cmd = f'adb shell am force-stop {self.get_packname()}'
        os.popen(cmd)
        self.print_text(f'手动强停{self.force_stop_num}次')

    # 实时更新图
    def start_plot(self):
        self.wrong_tip(self.get_packname())
        self.i = 0
        self.x = [0]
        self.y = [0]
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.updateData)
        self.update_timer.start(1000)  # 1000ms更新一次
        thread = threading.Thread(target=self.updateData())
        thread.start()

    def updateData(self):
        self.old_pid = self.y[-1]
        self.i += 1
        self.x.append(self.i)
        self.y.append(float(self.pid_now()))

        # 更新绘图
        self.ui.historyPlot.clear()
        self.ui.historyPlot.plot(self.x, self.y)
        self.ui.X_line.setText('')
        self.ui.X_line.setText(str(self.x[-1]))
        self.ui.Y_line.setText('')
        self.ui.Y_line.setText(str(self.y[-1]))
        self.ui.time_line.setText('')
        self.ui.time_line.setText(str(datetime.datetime.now().strftime("%H:%M:%S")))
        self.last_pid = self.y[-1]
        thread = threading.Thread(target=self.reset_process, args=(self.last_pid, self.old_pid))
        thread.start()

    # 进程重置节点记录
    def reset_process(self, last_pid, old_pid):
        if int(old_pid) == 0:
            pass
        elif str(last_pid) != str(old_pid) and int(last_pid) != 0:
            self.reset_process_num += 1
            self.print_text(f'进程重启{self.reset_process_num}次\n')
        else:
            pass

    def uninstall(self):
        self.wrong_tip(self.get_packname())
        cmd = f'adb uninstall {self.get_packname()}'
        result = os.popen(cmd)
        self.print_text(str(result.read()))

    def install_apk(self):
        self.wrong_tip(self.get_apkpath())
        cmd = f'adb install {self.get_apkpath()}'
        result = os.popen(cmd)
        self.print_text(str(result.read()))
        self.ui.packname_input.setText(str(GetInfo().get_appPackagename(self.apppath)))
    def debug_install_t(self):
        self.wrong_tip(self.get_apkpath())
        thread = threading.Thread(target=self.debug_install)
        thread.start()

    def debug_install(self):
        debugpath = r'D:\to'
        self.apppath = self.ui.apk_path.text()
        apppath = str(self.apppath).replace('"', '')
        get = GetInfo()
        device = u2.connect_usb(get.get_deviceids())
        acti = activiting(device)
        self.print_text(acti.install_and_debug(apppath, debugpath))
        self.ui.packname_input.setText(str(GetInfo().get_appPackagename(self.apppath)))


if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    sys.exit(app.exec_())
