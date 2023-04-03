import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import numpy as np
# from pip._vendor.distlib._backport import shutil

from datetime import datetime
import shutil
import os
import time
import datetime
import uiautomator2 as u2
# from tools.Tabular_parameterization.table_parameter import Parameter
from aotudriver.get_info import GetInfo
from aotudriver import LayoutData


# apppatn = r'C:\Users\Administrator\Desktop\yxtest\38373008_cn.dtandroiduc.dpyctssquare_1.0.0_vitxzn_20211102.apk'
class AotuDriver(object):
    def __init__(self, device, apppatn=None):
        # 对象级属性
        self.device = device
        self.device.implicitly_wait(20)
        self.get_info = GetInfo()
        self.LayoutData = LayoutData()
        # self.para = Parameter()
        # 参数级属性
        self.phone_info = None
        # 当前时间
        self.time_H = self.get_info.get_current_timeH()
        self.time_HM = self.get_info.get_current_timeHM()
        self.time_YMD = self.get_info.get_current_timeYMD()
        # 强停所有进程
        # self.device.app_stop_all()
        # self.device = u2.connect_usb(self.deviceid)
        # 创建一个日期文件夹，在根据日期文件夹创建时间文件夹
        # 纯净截图
        # self.pathYTD_c = self.create_folder_YTD(self.LayoutData.tupianpath_C)
        # self.pathHMS_c = self.create_folder_HMS(self.pathYTD_c)
        # 病毒截图
        # self.pathYTD_v = self.create_folder_YTD(self.LayoutData.tupianpath_V)
        # self.pathHMS_v = self.create_folder_HMS(self.pathYTD_v)
        # 病毒包
        # self.virus_YTD = self.create_folder_YTD(self.LayoutData.virus)
        time.sleep(5)
        # 进程守护
        # self.healthcheck()
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

    # 发送邮件
    def sendmail(self, conntent, conntent2, conntent3, theme, Email_user):
        msg_from = '502985007@qq.com'  # 发送方邮箱
        passwd = 'nibagizkcbbgbiih'  # 就是上面的授权码
        to = [Email_user]  # 接受方邮箱
        # 设置邮件内容
        # MIMEMultipart类可以放任何内容
        msg = MIMEMultipart()
        # conntent = "这个是字符串"
        # 把内容加进去
        msg.attach(MIMEText(conntent, 'plain', 'utf-8'))
        msg.attach(MIMEText(conntent2, 'plain', 'utf-8'))
        msg.attach(MIMEText(conntent3, 'plain', 'utf-8'))

        # 设置邮件主题
        msg['Subject'] = theme
        # 发送方信息
        msg['From'] = msg_from
        # 开始发送
        # 通过SSL方式发送，服务器地址和端口
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登录邮箱
        s.login(msg_from, passwd)
        # 开始发送
        s.sendmail(msg_from, to, msg.as_string())

    # 在指定目录下根据当前年月日创建一个文件夹，在根据当前时间创建一个文件并返回路径
    def full_save_folder(self, path):
        folder_YTD = self.create_folder_YTD(path)
        if self.time_HM in folder_YTD:
            return fr'{folder_YTD}\{self.time_HM}'
        else:
            return self.create_folder_HMS(folder_YTD)

    # 根据年月日/时分秒/手机设备创建文件目录
    def full_phone_file(self, pata):
        folderName = self.full_save_folder(pata)
        if str(self.phone_info) in self.get_info.get_dirs_name(folderName):
            folderName = fr'{folderName}\{self.phone_info}'
            return folderName
        else:
            folderName = fr'{folderName}\{self.phone_info}'
            os.makedirs(folderName)
            return folderName

    # 在指定目录下根据当前年月日创建一个文件夹并返回绝对路径
    def create_folder_YTD(self, path):
        """
        在指定目录下根据当前年月日创建一个文件夹，如果有了这个这个文件夹将不在创建
        :param path1:
        :param path5:
        :param pathname: 绝对路径
        :return: 返回已经创建完成文件夹的绝对路径
        """
        timename = datetime.datetime.now().strftime('%Y年%m月%d日')
        if timename in self.get_info.get_dirs_name(path):
            folderName = fr'{path}\{timename}'
            return folderName
        else:
            folderName = fr'{path}\{timename}'
            os.makedirs(folderName)
            return folderName

    # 在指定目录下根据当前年月日创建一个文件夹并返回绝对路径
    def create_folder_HMS(self, path):
        """
        在指定目录下根据当前年月日创建一个文件夹，如果有了这个这个文件夹将不在创建
        :param path1:
        :param path5:
        :param pathname: 绝对路径
        :return: 返回已经创建完成文件夹的绝对路径
        """
        if self.time_HM in self.get_info.get_dirs_name(path):
            folderName = fr'{path}\{self.time_HM}'
            return folderName
        else:

            folderName = fr'{path}\{self.time_HM}'
            os.makedirs(folderName)
            return folderName

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

    # 将毒包移动到指定文件夹
    def save_virus_package(self, virus_package_list, from_path, to_path):
        for virus in virus_package_list:
            shutil.move(rf'{from_path}\{virus}',
                        fr'{to_path}')

    # 需要使用安卓驱动的方法

    #   灭屏/亮屏,解锁
    def applications(self):
        # 灭屏/亮屏,解锁
        self.device.screen_off()
        time.sleep(1)
        self.device.screen_on()
        time.sleep(3)
        self.device.swipe_points([(0.485, 0.708), (0.481, 0.286)], 0.05)
        print('解锁成功')

    # 截图方法
    def screenshot(self, savePath, pictureName):
        self.device.screenshot(fr'{savePath}\{pictureName}.png')

    #   vivo机型进入手机文件夹方法apk文件夹方法
    def Entering_storage_space(self):
        """
        vivo机型进入手机文件夹方法apk文件夹方法
        :return: 空
        """
        # os.system(f'adb shell am force-stop com.android.filemanager')
        self.device.app_stop('com.android.filemanager')
        self.device.app_start('com.android.filemanager', use_monkey=True)
        self.click('text', '稍后提醒', 2)
        # 点击手机存储
        self.device(resourceId='com.android.filemanager:id/title').click()
        self.device(text='排序').click()
        self.device(text='按名称').click()
        self.device(text='apk').click()
        self.device(text='排序').click()
        self.device(text='按时间升序').click()

    # 查找元素并返回结果True and False
    def is_findElement(self, type, Settings, time=10.0):
        """
        查找元素并返回
        :param type: 元素类型
        :param Settings: 元素关键字
        :param time:  超时时间
        :return: 返回结果
        """
        if type == 'text':
            return self.device(text=Settings).wait(timeout=time)
        elif type == 'resourceId' or type == 'Rid':
            return self.device(resourceId=Settings).wait(timeout=time)
        elif type == 'textContains' or type == 'LikeText':
            return self.device(textContains=Settings).wait(timeout=time)
        elif type == 'className' or type == 'Cn':
            return self.device(textContains=Settings).wait(timeout=time)
        else:
            print('检查元素类型')

    def get_text_auto(self, type, Settings):
        """
                查找元素并返回
                :param type: 元素类型
                :param Settings: 元素关键字
                :param time:  超时时间
                :return: 返回结果
                """
        if type == 'text':
            return self.device(text=Settings).get_text()
        elif type == 'resourceId' or type == 'Rid':
            return self.device(resourceId=Settings).get_text()
        elif type == 'textContains' or type == 'LikeText':
            return self.device(textContains=Settings).get_text()
        elif type == 'className' or type == 'Cn':
            return self.device(className=Settings).get_text()
        else:
            print('检查元素类型')

    def get_text_new(self, **kwargs):
        """
        获取元素文本信息
        :param timeout: 超时时间
        :param kwargs: 元素定位
        :return:
        """
        return self.device(**kwargs).get_text()

    def get_device_info(self):
        """
        获取设备信息
        :return:
        """
        return self.device.info

    def swipe_down_screen(self):
        """
        向下滑动屏幕，默认为一屏
        :param scre: 滑动比例
        :return:
        """
        self.device.swipe_points([(0.3, 0.9), (0.3, 0.2)], 0.5)

    # 点击元素
    def click(self, type, Settings, time=15.0):
        """
            点击元素并
        :param type: 元素类型
        :param Settings: 元素关键字
        :param time:  超时时间默认5秒
        :return: 返回空
        """

        if self.is_findElement(type, Settings, time):
            if type == 'text' and self.is_findElement(type, Settings, time) != 0:
                self.device(text=Settings).click(timeout=time)
            elif type == 'resourceId' or type == 'Rid':
                self.device(resourceId=Settings).click(timeout=time)
            elif type == 'textContains' or type == 'LikeText':
                self.device(textContains=Settings).click(timeout=time)
            elif type == 'className' or type == 'Cn':
                self.device(className=Settings).click(timeout=time)
            else:
                print('检查元素类型')

    def input_text(self, type, Settings, time, value):
        """
            点击元素并
        :param type: 元素类型
        :param Settings: 元素关键字
        :param time:  超时时间默认5秒
        :return: 返回空
        """
        if self.is_findElement(type, Settings, time):
            if type == 'text':
                self.device(text=Settings).click(timeout=time)
                self.device(text=Settings).send_keys(value)
                self.device.press("enter")
            elif type == 'resourceId' or type == 'Rid':
                self.device(resourceId=Settings).click(timeout=time)
                self.device.send_keys(value)
                self.device.press("enter")
            elif type == 'textContains' or type == 'LikeText':
                self.device(textContains=Settings).click(timeout=time)
                self.device(textContains=Settings).send_keys(value)
                self.device.press("enter")
            elif type == 'className' or type == 'Cn':
                self.device(className=Settings).click(timeout=time)
                self.device(className=Settings).send_keys(value)
                self.device.press("enter")
            else:
                print('检查元素类型')

    # 指定元素拖到中间
    def drag_to_centre(self, type, Settings, time=5):
        """
            点击元素并
        :param type: 元素类型
        :param Settings: 元素关键字
        :param time:  超时时间
        :return: 返回空
        """
        if self.is_findElement(type, Settings, time):
            if type == 'text':
                self.device(text=Settings).drag_to("centre", duration=0.3)
            elif type == 'resourceId' or type == 'Rid':
                self.device(resourceId=Settings).drag_to("centre", duration=0.3)
            elif type == 'textContains' or type == 'LikeText':
                self.device(textContains=Settings).drag_to("centre", duration=0.3)
            elif type == 'className' or type == 'Cn':
                self.device(textContains=Settings).drag_to("centre", duration=0.3)
            else:
                print('检查元素类型')
        else:
            pass

    # 右滑动解锁成功
    def Lock_screen_press(self, pathsucceed, pathloser):
        self.device.swipe_points([(0.2, 0.5), (0.8, 0.5)], 0.5)
        print(f'{self.time_HM}:右滑动解锁成功')
        if self.is_findElement('LikeText', '优化中', 30):
            print(f'{self.time_HM}:弹窗动画展示成功立即截图保存')
            self.screenshot(pathsucceed, f'{self.time_HM}_解锁后动画.png')
            print(f'{self.time_HM}:等待广告加载')
            time.sleep(30)
            self.screenshot(pathsucceed, f'{self.time_HM}_视频广告.png')
            print(f'{self.time_HM}:截图成功')
            # self.succeed_num += 1
            # return self.succeed_num
        else:
            print(f'{self.time_HM}:解锁后动画展示失败')
            self.screenshot(pathloser, f'{self.time_HM}_解锁后动画失败.png')
            # self.loser_num += 1
            # return self.loser_num

        # 右滑动解锁成功

    # def AD_screenshot(self):
    #     if self.device(text='正在进行优化').wait_gone(timeout=20):
    #         # print(f'{self.time_HM}等待广告加载')
    #         if self.is_findElement('text', '反馈', 50):
    #             print(f'{self.phone_info}广告展示成功，截图保存')
    #             self.screenshot(self.LayoutData.ggjietu, f'{self.time_HM}_广告截图.png')
    #             # 点击关闭
    #             time.sleep(30)
    #             self.click('text', '跳过', 0.5)
    #             self.device.click(0.891, 0.041)
    #             self.device.click(0.886, 0.074)
    #         else:
    #             print(f'{self.phone_info}广告加载失败')
    #             self.screenshot(self.LayoutData.ggjietu_lose, f'{self.time_HM}_广告加载失败截图.png')

    def end_animation(self):
        if self.is_findElement('text', '急速wifi', 30):
            print(f'{self.time_HM}解锁后落地页展示成功')
            self.screenshot(self.LayoutData.end, f'{self.time_HM}_落地页展示成功截图.png')
        else:
            print(f'{self.time_HM}解锁后落地页展示失败')
            self.screenshot(self.LayoutData.end_lose, f'{self.time_HM}_后落地页展示失败截图.png')

    def app_start_aotu(self, appname):
        self.device.app_start(appname, use_monkey=True)

    #  锁屏
    def applications_test(self, keyword):
        # 灭屏/亮屏,解锁
        self.device.screen_off()
        time.sleep(2)
        self.device.screen_on()
        time.sleep(2)
        # 向上滑动解锁
        self.device.swipe_points([(0.485, 0.708), (0.481, 0.286)], 0.05)
        # 判断是否出现
        if self.is_findElement('text', '推荐'):
            print(f'{keyword}:锁屏新闻展示成功')
            time.sleep(5)
            # 返回路径
            # return f'{pathsucceed}\{time_HM}_{keyword}_锁屏新闻.png'
            return True
        else:
            print(f'{keyword}:锁屏新闻展示失败')
            # return f'{pathlose}\{time_HM}_{keyword}_锁屏新闻失败.png'
            return False

    #  锁屏测试
    def applications_save(self, pathsucceed, pathlose, time_HM, keyword):
        # 灭屏/亮屏,解锁
        self.device.screen_off()
        time.sleep(1)
        self.device.screen_on()
        time.sleep(2)
        # 向上滑动解锁
        self.device.swipe_points([(0.485, 0.708), (0.481, 0.286)], 0.05)
        # 判断是否出现
        if self.is_findElement('text', '推荐'):
            print(f'{keyword}:锁屏新闻展示成功')
            time.sleep(5)
            self.screenshot(pathsucceed, f'{time_HM}_{keyword}_锁屏新闻成功')
            # 返回路径
            # return f'{pathsucceed}\{time_HM}_{keyword}_锁屏新闻.png'
            return True
        else:
            print(f'{keyword}:锁屏新闻展示失败')
            self.screenshot(pathlose, f'{time_HM}_{keyword}_锁屏新闻失败')
            # return f'{pathlose}\{time_HM}_{keyword}_锁屏新闻失败.png'
            return False

    # 解锁后动画
    def New_animation_test(self, keyword):
        # el = 'cn.dwkandroidrwd.hypctsoptic:id/ump'
        self.device.swipe_points([(0.2, 0.5), (0.8, 0.5)], 0.5)
        if self.is_findElement('text', '深度优化', 1) or self.is_findElement('text', '稍后操作') or self.is_findElement('text',
                                                                                                                '手机卫士'):
            print(f'{keyword}:解锁后动画展示成功')
            time.sleep(1)
            return True
        else:
            print(f'{keyword}:解锁后动画展示失败')

            return False

    # 解锁后动画
    def New_animation(self, pathsucceed, pathloser, time_HM, keyword):
        el = 'com.oeaandroiduf.fckctseasy:id/ggl'
        self.device.swipe_points([(0.2, 0.5), (0.8, 0.5)], 0.5)
        if self.is_findElement('Rid', el):  # self.is_findElement('text', '清理')self.is_findElement('text', '深度优化') or
            print(f'{keyword}:弹窗动画展示成功')
            time.sleep(1)
            self.screenshot(pathsucceed, f'{time_HM}_{keyword}_解锁后动画成功')
            # self.click('text', '深度优化', 1)
            # self.click('text', '清理', 0.1)
            # 这里会导致站内动画判断时间太短
            self.click('Rid', el)
            # return f'{pathsucceed}\{time_HM}_{keyword}_解锁后动画.png'
            return True
        else:
            print(f'{keyword}:解锁后动画展示失败')
            self.screenshot(pathloser, f'{time_HM}_{keyword}_解锁后动画失败')
            # return f'{pathloser}\{time_HM}_{keyword}_解锁后动画失败.png'
            return False

    # 站内动画
    def unlock_animation(self, pathsucceed, pathloser, time_HM, keyword):
        if self.is_findElement('LikeText', '正在进行优化:', 0.6) or self.is_findElement('Rid',
                                                                                  'cn.dtandroiduc.dpyctssquare:id/j2g',
                                                                                  1):
            print(f'{keyword}：站内动画展示成功')
            self.screenshot(pathsucceed, f'{time_HM}_{keyword}_站内动画成功')
            # return f'{pathsucceed}\{time_HM}_{keyword}_站内动画成功.png'
            return True
        else:
            print(f'{keyword}:站内动画展示失败')
            self.screenshot(pathloser, f'{time_HM}_{keyword}_站内动画失败')
            # return f'{pathloser}\{time_HM}_{keyword}_站内动画失败.png'
            return False

    # 视频广告
    def AD_screenshot(self, pathsucceed, pathloser, time_HM, keyword):
        if self.device(text='正在进行优化').wait_gone(timeout=20):
            # print(f'{keyword}等待广告加载')
            if self.is_findElement('text', '反馈', 50):
                print(f'{keyword}广告展示成功')
                self.screenshot(pathsucceed, f'{time_HM}_{keyword}_广告加载成功')
                # print(f'{keyword}：广告播放中，请等待.......')
                # 点击关闭
                time.sleep(15)
                self.click('text', '跳过', 0.5)
                self.device.click(0.891, 0.041)
                self.device.click(0.886, 0.074)
                self.device.press('back')
                self.device.press('home')
                self.device.press('back')
                # return f'{pathsucceed}\{time_HM}_{keyword}_广告加载成功截图.png'
                return True
            else:
                print(f'{keyword}广告加载失败')
                self.screenshot(pathloser, f'{time_HM}_{keyword}_广告加载失败截图')
                # return f'{pathsucceed}\{time_HM}_{keyword}_广告加载失败截图.png'
                self.device.press('back')
                self.device.press('home')
                self.device.press('back')
                return False

    # 通过USB连接设备
    def connect_usb(self):
        """
        通过USB连接设备
        :return:
        """
        return u2.connect_usb()

    #   检查并维持设备端守护进程处于运行状态
    def healthcheck(self):
        """
        检查并维持设备端守护进程处于运行状态
        :return:
        """
        self.device.healthcheck()

    # 清除app缓存
    def app_clear(self, package_name):
        """
        清除app缓存
        :param package_name: 应用包名
        :return:
        """
        return self.device.app_clear(package_name)

    # 关闭excludes中的所有应用
    def app_stop_all(self, excludes):
        """
        关闭excludes中的所有应用
        :param excludes: 应用包名集合
        :return:
        """
        self.device.app_stop_all(excludes)

    # 关闭app
    def app_stop(self, package_name):
        """
        关闭app
        :param package_name: 应用包名
        :return:
        """
        self.device.app_stop(package_name)

    # 卸载应用
    def app_uninstall(self, package_name):
        """
        卸载应用
        :param package_name: 应用包名
        :return:
        """
        self.device.app_uninstall(package_name)

    # 安装app
    def app_install(self, path):
        """
        安装应用
        :param package_name: 应用包名
        :return:
        """
        self.device.app_install(path)

    # 获取设备信息
    def get_phone_info(self, is_tuple=True, is_print=False):
        """
        :return: 安卓版本手机型号手机品牌
        """
        list_info = []
        info_d = self.device.device_info
        # print(info_d)
        info_d = dict(info_d)
        fieldName = []
        phone_value = []
        for k, v in info_d.items():
            fieldName.append(k)
            phone_value.append(v)
        # 获取安卓版本，手机型号，手机品牌
        android_version = phone_value[1]
        phone_brand = phone_value[3]
        phone_model = phone_value[4]
        list_info.append(phone_brand), list_info.append(phone_model), list_info.append(android_version)
        if is_print:
            print('设备信息如下：')
            print(f'安卓版本：{android_version} 手机型号：{phone_model} 手机品牌：{phone_brand}')
        if is_tuple:
            return phone_brand, phone_model, android_version
        else:
            return list_info

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

    def opop_dian(self):
        self.device.implicitly_wait(20)
        """
        处理oppo手机安装应用时出现的安装弹窗,这里写死安装应用时如果出现要输入安装密码,,则去配置文件中寻找本次测试设备对应的安装密码,配置中没有则会使用dn123123
        :return: None
        """
        time.sleep(10)
        oppo_passwd_edit_element = {"resourceId": 'com.coloros.safecenter:id/et_login_passwd_edit'}
        oppo_install_button = {'resourceId': 'android:id/button1', 'text': '安装'}
        oppo_install_button1 = {'resourceId': 'com.android.packageinstaller:id/install_confirm_panel'}
        oppo_install_button2 = {'text': '我已知问题严重性。无视风险安装'}
        oppo_install_button3 = {
            'resourceId': 'com.android.packageinstaller:id/bottom_button_layout'}  # oppo商店安装页面实际安装按钮在上面？
        oppo_install_button3_1 = {
            'resourceId': 'com.android.packageinstaller:id/safe_button_layout'}  # oppo商店安装页面实际安装按钮在下面
        oppo_install_button4 = {'textMatches': '^继续安装$|^安装$'}
        oppo_install_button5 = {'resourceId': 'com.android.packageinstaller:id/btn_app_store_safe'}

        if self.device(**oppo_passwd_edit_element).exists():
            # log.info(f'出现安装弹窗,输入密码: {self.__install_pwd}, 并点击安装')
            print(f'出现安装弹窗,输入密码 并点击安装')
            self.device(**oppo_passwd_edit_element).set_text('dn123123')
            self.device(**oppo_install_button).click()
        time.sleep(5)
        if self.device(**oppo_install_button3).exists:
            self.device(**oppo_install_button3).click(offset=(0.5, 0.4))
        time.sleep(5)
        if self.device(**oppo_install_button3_1).exists:
            self.device(**oppo_install_button3_1).click(offset=(0.5, 0.9))
        time.sleep(5)

        if self.device(**oppo_install_button1).exists:
            self.device(**oppo_install_button1).click(offset=(0.5, 0.98))
        time.sleep(5)
        if self.device(**oppo_install_button4).exists:
            # log.info(f'点击: {self.device(**oppo_install_button4).get_text()}')
            self.device(**oppo_install_button4).click_exists()
        time.sleep(5)
        if self.device(**oppo_install_button2).exists:
            print('出现安装风险,点击无视风险安装')
            self.device(**oppo_install_button2).click(offset=(0.8, 0.4))

    def install_click(self):
        if self.is_findElement('text', '忘记密码', 30):
            print('出现密码弹窗')
            self.device.send_keys('dn123123')
            self.click('text', '安装')
        print(f"正在扫描：{self.is_findElement('LikeText', '正在扫描')}")
        if self.is_findElement('LikeText', '人工亲测'):
            print('处理OPPO商店安装页面')
            self.device.click(0.764, 0.94)
            time.sleep(1)
            self.device.click(0.501, 0.868)
        if self.is_findElement('LikeText', '应用权限'):
            print('到达安装页面直接点击安装')
            self.device.click(0.501, 0.855)
            self.device.click(0.501, 0.91)
            self.device.click(0.501, 0.948)

    def press_home(self):
        """
        按home键
        :return:
        """
        self.device.press("home")

    def press_back(self):
        """
        按返回键
        :return:
        """
        self.device.press("back")

    def press(self, key):
        """
        按下键码
        :param key: 键码值
        :return:
        """
        self.device.press(key)

    def press_enter(self):
        """
        按下回车键
        :return:
        """
        self.device.press.enter()

    def custom_print(self, keyword, color=34):
        # 34蓝色|37灰|31红色|32绿色
        print(f"\033[1;{color};40m{keyword}\033[0m")

    def exists(self, timeout=30.0, **kwargs):
        """
        判断元素是否存在
        :param timeout: 超时时间
        :param kwargs: 元素定位
        :return:
        """
        return self.device(**kwargs).exists(timeout=timeout)

    def wait_activity(self, activity, timeout=10):
        """
        等待activity加载出来
        :param activity:
        :param timeout:
        :return:
        """
        return self.device.wait_activity(activity=activity, timeout=timeout)

    def get_count(self, **kwargs):
        """
        获取元素个数
        :param kwargs: 元素定位
        :return:
        """
        return self.device(**kwargs).count
