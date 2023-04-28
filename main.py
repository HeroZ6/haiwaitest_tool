import json
import threading
from subprocess import Popen
from tools import QEventHandler
from tools import tool
from cfg.cfg import endecode_url
import qtmodern.styles
import uiautomator2 as u2
from PySide2.QtWidgets import QApplication, QMessageBox, QTextBrowser, QWidget
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


class MySignals(QThread):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    update_signal = Signal(list, list)
    line_signal = Signal(list, list, str, str)
    time_signal = Signal(str)
    reset_process = Signal(str)

    def __init__(self):
        super().__init__()
        self.i = 0
        self.y = [0]
        self.x = [0]
        self.reset_process_num = 0

    def run(self):
        self.i = 0
        self.y = [0]
        self.x = [0]

        def pid_now():
            packagename = stats.get_packname()
            pid_cmd = f'adb shell ps|findstr {packagename}'
            pid_content = os.popen(pid_cmd).read()
            p = re.compile(packagename)
            num = len(p.findall(pid_content))

            if str(packagename) in pid_content:
                p = re.compile(' (\d.*?) ')
                pid = p.findall(pid_content)[0]
            else:
                pid = 0
            return pid, pid_content, num

        while True:
            self.i += 1
            self.old_pid = self.y[-1]
            self.x.append(self.i)
            self.y.append(int(pid_now()[0]))
            self.last_pid = self.y[-1]
            self.update_signal.emit(self.x, self.y)
            self.line_signal.emit(self.x, self.y, str(datetime.datetime.now().strftime("%H:%M:%S")), str(pid_now()[2]))
            if int(self.old_pid) == 0:
                pass
            elif str(self.last_pid) != str(self.old_pid) and int(self.last_pid) != 0:
                self.reset_process_num += 1
                self.reset_process.emit(f'进程重启{self.reset_process_num}次\n')
            else:
                pass

            self.msleep(int(stats.get_interval()) * 1000)


# 实例化
mysi = MySignals()


# 清理数据线程
class clearSignals(QThread):
    clear_signals = Signal(str)
    device_refresh = Signal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        self.l = 30
        while True:
            if int(self.l) <= int(30):
                self.clear_signals.emit(str(f'{self.l}'))
                self.l -= 1
                if int(self.l) == 0:
                    self.l = 30
                    self.device_refresh.emit(1)
            self.msleep(1000)


clearqt = clearSignals()


class checkSignals(QThread):
    check_signals = Signal(str)
    key_query_signals = Signal(str, str, str)
    aab_query_signals = Signal(str, str, str)
    check_result_signls = Signal(str)

    def __init__(self, param):
        super().__init__()
        self.param = param

    def query_key(self):
        key_path = check.chcek_ui.key_path.text()
        pwd = check.chcek_ui.pwd.text()
        try:
            if key_path != None and pwd != None:
                key_query = tool.get_keystoreSha(key_path, pwd)
                self.key_query_signals.emit(key_query[0], key_query[1], key_query[2])
        except IndexError:
            self.key_query_signals.emit('请检查密码是否正确且不能为空！！', None, None)

    def query_aab(self):
        aab_path = check.chcek_ui.aab_path.text()
        try:
            if aab_path != None:
                aab_query = tool.get_aabkeystoreSha(aab_path)
                self.aab_query_signals.emit(aab_query[0], aab_query[1], aab_query[2])
        except IndexError:
            self.aab_query_signals.emit('请检查路径是否正确且不能为空！！', None, None)

    def compare_sha(self):
        try:
            key_path = check.chcek_ui.key_path.text()
            pwd = check.chcek_ui.pwd.text()
            aab_path = check.chcek_ui.aab_path.text()
            aab = tool.get_aabkeystoreSha(aab_path)

            if aab[0] and aab[1] and aab[2] not in tool.get_keystoreSha(key_path, pwd):
                self.check_result_signls.emit('匹配失败')
            elif aab[0] and aab[1] and aab[2] in tool.get_keystoreSha(key_path, pwd):
                self.check_result_signls.emit('匹配成功')
        except IndexError:
            self.check_result_signls.emit('数据获取不完整，无法匹配')

    def run(self):
        if int(self.param) == 0:
            self.query_key()
        elif int(self.param) == 1:
            self.query_aab()
        elif int(self.param) == 2:
            self.compare_sha()


# compare_sha(key_path, aab_path)


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
        loader = QUiLoader()
        loader.registerCustomWidget(pg.PlotWidget)

        self.ui = QUiLoader().load(r'D:\protect\haiwaitest_v0.8\ui\main.ui')
        self.ui.setWindowTitle('haiwai_tools')
        # 初始化按钮状态
        self.ui.stop_button.setEnabled(False)
        self.ui.process_start.setEnabled(True)
        self.ui.start_time.setEnabled(True)
        self.ui.reset.setEnabled(False)
        # 按钮连接
        # 环境检测
        self.ui.env_button.clicked.connect(self.get_device_info)
        # 清除上结果框
        self.ui.clear_button.clicked.connect(self.clear_result)
        # 进程监控绘图
        self.ui.process_start.clicked.connect(self.start_plot)
        # 清除绘图数据
        self.ui.process_clear.clicked.connect(self.clear_process)
        # 停止绘图进程
        self.ui.stop_button.clicked.connect(self.stop_timer)
        # 强停app
        self.ui.force_stop.clicked.connect(self.force_stop)
        # 卸载app
        self.ui.uninstall_bt.clicked.connect(self.uninstall)
        # 直接安装
        self.ui.common_install.clicked.connect(self.install_apk_t)
        # debug安装
        self.ui.debug_install.clicked.connect(self.debug_install_t)
        # 获取路径
        self.ui.auto_getpath.clicked.connect(self.get_path)
        # 获取设备
        self.ui.refresh.clicked.connect(self.get_devices)
        # 倒计时
        self.ui.start_time.clicked.connect(self.count_down_t)
        # 时间重置
        self.ui.reset.clicked.connect(self.time_reset)
        # 解码
        self.ui.encode_bt.clicked.connect(self.endecode)
        # 打开签名检验界面
        self.ui.key_input.clicked.connect(self.open_check)
        self.ui.apk_path.installEventFilter(QEventHandler(self.ui.apk_path))

    ##=============================================================tab1=============================================================##

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
        # try:
        content = str(self.ui.result_label.toPlainText())
        p = re.compile('(?<=file:///).+')
        self.fpath = p.findall(content)
        self.ui.apk_path.setText(self.fpath[0])
        self.ui.result_label.clear()
        p1 = re.compile('_(.*?)_')
        packname = p1.findall(content)[0].replace('_', '')
        self.ui.packname_input.setText(str(packname))
        # self.ui.packname_input.setText(tools.get_packname2(self.fpath))
        # except:
        self.ui.packname_input.setText('非规范文件名,安装后获取包名')

    # 错误弹窗
    def wrong_tip(self, path):
        if str(path) == '':
            self.tips_windows.critical(
                self.ui,
                '错误',
                '路径不能为空！')
            self.ui.stop_button.setEnabled(False)
            self.ui.process_start.setEnabled(True)
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
            p = re.compile(' (\d.*?) ')
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
        self.ui.proce_result.clear()

    # 进程栏
    def clear_process(self):
        self.ui.historyPlot.clear()
        self.ui.X_value1.clear()
        self.ui.Y_value1.clear()
        self.ui.time_now.clear()
        self.ui.pid_c.clear()

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
        self.clear_thread.terminate()
        self.plot_thread.terminate()  # 停止 QTimer
        self.ui.process_start.setEnabled(True)
        self.ui.stop_button.setEnabled(False)
        self.ui.historyPlot.setMouseEnabled(x=True, y=True)  # 鼠标xy都不能划动

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
        # self.open_mainwindow2()
        self.ui.X_value1.clear()
        self.ui.Y_value1.clear()
        self.ui.time_now.clear()
        self.ui.pid_c.clear()
        self.ui.historyPlot.clear()
        self.ui.stop_button.setEnabled(True)
        self.ui.process_start.setEnabled(False)
        self.ui.historyPlot.setMouseEnabled(x=False, y=False)  # 鼠标xy都不能划动
        self.l = 30
        self.wrong_tip(self.get_packname())
        # self.i = 0
        # self.x = [0]
        # self.y = [0]

        self.plot_thread = mysi
        self.clear_thread = clearqt
        self.plot_thread.update_signal.connect(self.plot)
        self.plot_thread.line_signal.connect(self.line)
        self.plot_thread.reset_process.connect(self.reset_report)
        self.clear_thread.clear_signals.connect(self.clear_time)
        self.clear_thread.device_refresh.connect(self.get_devices)
        self.plot_thread.start()  # 1000ms更新一次
        self.clear_thread.start()

    def clear_plot(self):
        self.ui.historyPlot.clear()
        print(f'{datetime.datetime.now().strftime("%H:%M:%S")}\n清除一次\n')

    # ====================================================主线程更新ui-start===============================================================##

    def clear_time(self, str1):
        self.ui.clear_time.setText(str1)

    def reset_report(self, str):
        self.print_text2(str)

    def line(self, list1, list2, str3, str4):
        self.ui.X_value1.setText(str(list1[-1]))
        self.ui.Y_value1.setText(str(list2[-1]))
        self.ui.time_now.setText(str3)
        self.ui.pid_c.setText(str4)

    def plot(self, list1, list2):
        self.curve = self.ui.historyPlot.plot()
        self.curve.setData(list1, list2)

    # ====================================================主线程更新ui-end===============================================================##

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
                f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}\n==============logs=================\ndebug安装失败,请重试或检查路径是否正确\n')

    # def open_mainwindow2(self):
    #
    #     stats2.ui2.show()
    #     app.exec_()

    ##=============================================================tab2=======================================##

    def endecode(self):
        self.ui.input_msg.clear()
        content = self.ui.decode_msg.toPlainText()
        res = requests.get(content)
        vlaue = res.json()['data']
        url = endecode_url + vlaue
        res = requests.get(url)
        self.ui.input_msg.insertPlainText(res.text)

    def open_check(self):
        check.init()
        check.chcek_ui.show()
        app.exec_()


class Check(QWidget):
    def __init__(self):
        super().__init__()
        self.chcek_ui = QUiLoader().load(r'D:\protect\haiwaitest_v0.8\ui\checkui.ui')
        self.chcek_ui.query_key.clicked.connect(self.start_query_0)
        self.chcek_ui.query_aab.clicked.connect(self.start_query_1)
        self.chcek_ui.compare.clicked.connect(self.start_query_2)
        self.chcek_ui.key_path.installEventFilter(QEventHandler(self.chcek_ui.key_path))
        self.chcek_ui.aab_path.installEventFilter(QEventHandler(self.chcek_ui.aab_path))
        self.chcek_ui.clear_aab.clicked.connect(self.clear_query_1)
        self.chcek_ui.clear_key.clicked.connect(self.clear_query_0)
    def init(self):
        self.chcek_ui.check_result.clear()
        self.chcek_ui.key_sha1_re.clear()
        self.chcek_ui.key_sha256_re.clear()
        self.chcek_ui.key_md5_re.clear()
        self.chcek_ui.check_result.clear()
        self.chcek_ui.aab_sha1_re.clear()
        self.chcek_ui.aab_sha256_re.clear()
        self.chcek_ui.aab_md5_re.clear()
        self.chcek_ui.check_result.clear()

    def clear_query_0(self):
        self.chcek_ui.check_result.clear()
        self.chcek_ui.key_sha1_re.clear()
        self.chcek_ui.key_sha256_re.clear()
        self.chcek_ui.key_md5_re.clear()
        self.check_thread.terminate()
        self.chcek_ui.query_key.setEnabled(True)
        self.chcek_ui.query_aab.setEnabled(True)

    def clear_query_1(self):
        self.chcek_ui.check_result.clear()
        self.chcek_ui.aab_sha1_re.clear()
        self.chcek_ui.aab_sha256_re.clear()
        self.chcek_ui.aab_md5_re.clear()
        self.check_thread.terminate()
        self.chcek_ui.query_key.setEnabled(True)
        self.chcek_ui.query_aab.setEnabled(True)

    def start_query_0(self):
        self.chcek_ui.compare.setEnabled(False)
        self.chcek_ui.query_aab.setEnabled(False)
        self.check_thread = checkSignals(0)
        self.check_thread.start()
        self.check_thread.key_query_signals.connect(self.key_check_result)

    def start_query_1(self):
        self.chcek_ui.compare.setEnabled(False)
        self.chcek_ui.query_key.setEnabled(False)
        self.check_thread = checkSignals(1)
        self.check_thread.start()
        self.check_thread.aab_query_signals.connect(self.aab_check_result)

    def start_query_2(self):
        self.chcek_ui.query_key.setEnabled(False)
        self.chcek_ui.query_aab.setEnabled(False)
        self.check_thread = checkSignals(2)
        self.check_thread.start()
        self.check_thread.check_result_signls.connect(self.check_result)

    def key_check_result(self, str1, str2, str3):
        self.chcek_ui.key_sha1_re.setText(str1)
        self.chcek_ui.key_sha256_re.setText(str2)
        self.chcek_ui.key_md5_re.setText(str3)
        self.check_thread.terminate()
        self.chcek_ui.compare.setEnabled(True)
        self.chcek_ui.query_aab.setEnabled(True)


    def aab_check_result(self, str1, str2, str3):
        self.chcek_ui.aab_sha1_re.setText(str1)
        self.chcek_ui.aab_sha256_re.setText(str2)
        self.chcek_ui.aab_md5_re.setText(str3)
        self.check_thread.terminate()
        self.chcek_ui.compare.setEnabled(True)
        self.chcek_ui.query_key.setEnabled(True)

    def check_result(self, str1):
        self.chcek_ui.check_result.setText(str1)
        self.check_thread.terminate()
        self.chcek_ui.query_key.setEnabled(True)
        self.chcek_ui.query_aab.setEnabled(True)



class Stats2:
    def __init__(self):
        loader = QUiLoader()
        loader.registerCustomWidget(pg.PlotWidget)
        self.ui2 = QUiLoader().load(r'haiwaitest_tool_v0.8\ui\main2.ui')
        self.ui2.setWindowTitle('process')


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon(r'cfg\icon.ico'))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(r"cfg\icon.png")
    check = Check()
    stats = Stats()
    # stats2 = Stats2()
    qtmodern.styles.dark(app)
    stats.ui.show()
    sys.exit(app.exec_())
