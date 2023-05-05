
import subprocess

import time

from aotudriver.get_info import GetInfo
from aotudriver import LayoutData

class AotuDriver(object):
    def __init__(self, device, apppatn=None):
        # 对象级属性
        self.device = device
        self.device.implicitly_wait(20)
        self.get_info = GetInfo()
        self.LayoutData = LayoutData()
        # 参数级属性
        self.phone_info = None
        # 当前时间
        self.time_H = self.get_info.get_current_timeH()
        self.time_HM = self.get_info.get_current_timeHM()
        self.time_YMD = self.get_info.get_current_timeYMD()
        time.sleep(5)
        # 进程守护
        if apppatn:
            self.apkname = self.get_info.get_appPackagename(apppatn)

    def set_apkname(self, path):
        self.apkname = self.get_info.get_appPackagename(path)

    def get_apkname(self):
        return self.apkname

    def set_phone_info(self):
        # 这里需要处理下，如果不能转化成可读的信息，就不转化了
        # 利用参数化将手机型号变的可读
        # 型号转化成可读的型号
        phone_info_list = self.get_phone_info(is_tuple=False)
        datadict = self.para.get_data(r'D:\Mobile_phone_models_data\aircrafttypedata.xls')

        for k, v in datadict.items():
            if phone_info_list[1] == k:
                phone_info_list[1] = v
        # 修改实例属性值，设备信息
        self.phone_info = phone_info_list
        print('设备信息如下：')
        print(f'安卓版本：{self.phone_info[2]} 手机型号：{self.phone_info[1]} 手机品牌：{self.phone_info[0]}')
        return self.phone_info

    # 获取手机设备号列表,返回list
    def getphonelist(self):  # 获取手机设备
        cmd = r'adb devices'  # % apk_file
        pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        pr.wait()  # 不会马上返回输出的命令，需要等待
        out = pr.stdout.readlines()  # out = pr.stdout.read().decode("UTF-8")
        devices = []
        for i in (out)[1:-1]:
            device = str(i).split("\\")[0].split("'")[-1]
            devices.append(device)
        return devices  # 手机设备列表

    def set_implicitly_wait(self, timeout=30):
        """设置全局最长等待时间"""
        return self.device.implicitly_wait(timeout)

    # 等待点击
    def click_wait(self, timeout=10, **kwargs):
        """
        当timeout s内对象出现就点击
        :param timeout: 超时时间
        :param kwargs: 元素定位
        :return:
        """
        self.device(**kwargs).click_exists(timeout)

    # 安装app
    def app_install(self, path):
        """
        安装应用
        :param package_name: 应用包名
        :return:
        """
        self.device.app_install(path)
    def get_device_info(self):
        """
        获取设备信息
        :return:
        """
        return self.device.info

        # 定义传输文件方法，将电脑文件传入手机
    def Sending_files_from_your_phone(self, computer_file, phone_files):
        """
        将电脑文件传入手机
        :param computer_file: 电脑路径
        :param phone_files: 手机路径
        :return: 不返回值
        """
        filename_list = self.get_info.get_file_name(computer_file, False)
        print(filename_list)
        for filename in filename_list:
            self.device.push(rf"{computer_file}\{filename}", phone_files)
            print(f'{filename}传输成功')
            # print(f'{filename}传输失败')
        # else:
        #     print(f'文件传输完毕')

    # 获取设备序列号
    def get_serial(self):
        """
        :return: 序列号
        """
        info_d = self.device.device_info
        # print(info_d)
        info_d = dict(info_d)
        fieldName = []
        phone_value = []
        for k, v in info_d.items():
            fieldName.append(k)
            phone_value.append(v)
        # 获取安卓版本，手机型号，手机品牌
        version = phone_value[2]
        return version
