import subprocess
import os, re
from PySide2.QtCore import QCoreApplication, QObject, QRunnable, QThreadPool, QTimer, Qt, QCoreApplication
from pyqtgraph.Qt import QtCore
from ui import stats





# class Tool:
    # 在电脑上安装 ADB 工具，并且手机连接到电脑
    # 发送 ADB 命令获取手机的公网 IP 地址和设备信息
    # def get_device_info(self):
    #     try:
    #         ip_cmd = ['adb', 'shell', 'curl', 'ifconfig.me']
    #         ip_process = subprocess.Popen(ip_cmd, stdout=subprocess.PIPE)
    #         ip_address = ip_process.communicate()[0].decode().strip()
    #
    #         info_cmd = ['adb', 'shell', 'getprop', 'ro.product.model']
    #         info_process = subprocess.Popen(info_cmd, stdout=subprocess.PIPE)
    #         device_info = info_process.communicate()[0].decode().strip()
    #
    #         return ip_address, device_info
    #     except Exception as e:
    #         print("获取设备信息失败：", e)
    #         return None, None

    # def check_model(self):
    #     model = os.popen('adb shell getprop ro.product.model').read().strip()
    #     if model in ofiical_model:
    #         print(f'当前测试设备：\033[1;34m{model}\033[0m,对应产品：\033[1;34m{ofiical_product[model]}\033[0m')
    #     else:
    #         print('\033[1;41m危险测试设备,请更换设备.\033[0m')

    # def ip_location(self, ip):
    #     url = 'http://ip-api.com/json/' + ip
    #     response = urllib.request.urlopen(url).read().decode()
    #     data = json.loads(response)
    #     return data['country'] + ',' + data['regionName'] + ',' + data['city']





# if __name__ == "__main__":
    # ip_address, device_info = tool.get_device_info()
    # if ip_address and device_info:
    #     print("公网IP地址：", ip_address)
    #     print('地区：', tool.ip_location(ip_address))
    #     print("设备信息：", device_info)
    # else:
    # #     print("无法获取设备信息。")
    # tool = Tool()
    # packname = tool.get_packname()
