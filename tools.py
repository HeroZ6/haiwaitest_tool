import re, os
import subprocess
import sys
import time
from PySide2 import QtCore
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import requests
from PySide2.QtCore import Qt, QPoint, QEvent
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QMainWindow


class Tool:
    # aab和签名文件是否匹配
    def get_keystoreSha(self, key_path, pwd, work_path='C:\Program Files\Java'):
        try:
            content = subprocess.Popen(f'keytool -list -v -keystore {key_path} -storepass {pwd}',
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, cwd=work_path)
            out = content.communicate()[0].decode('gbk')
            p = re.compile('(?<=SHA1:).+')
            p2 = re.compile('(?<=SHA256:).+')
            key_Sha1 = p.findall(str(out))[0].strip()
            key_Sha256 = p2.findall(str(out))[0].strip()
            return key_Sha1, key_Sha256
        except NotADirectoryError as e:
            return e
        except IndexError as b:
            return b

    def get_aabkeystoreSha(self, aab_path, work_path='C:\Program Files\Java'):
        try:
            content = subprocess.Popen(f'keytool -printcert -jarfile {aab_path}', stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, cwd=work_path)
            out = content.communicate()[0].decode('gbk')
            p = re.compile('(?<=SHA1:).+')
            p2 = re.compile('(?<=SHA256:).+')
            aab_Sha1 = p.findall(str(out))[0].strip()
            aab_Sha256 = p2.findall(str(out))[0].strip()
            return aab_Sha1, aab_Sha256
        except IndexError as e:
            return e
    # aes解密

    # 定义PKCS7填充和反填充函数
    def pkcs7_padding(self, data):
        return pad(data, AES.block_size, style='pkcs7')

    def pkcs7_unpadding(self, data):
        return unpad(data, AES.block_size, style='pkcs7')

    # 定义AES解密函数
    def aes_decrypt(self, ciphertext, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        return self.pkcs7_unpadding(plaintext)

    def aes(self, url):
        # 加密后的数据
        RE = requests.get(url)
        aaa = RE.json()['data']
        ciphertext = base64.b64decode(aaa)
        # 密钥
        key = b'dwnxthekey902902'
        # 偏移量
        iv = b'dwnxthekey902902'
        # 解密数据
        plaintext = self.aes_decrypt(ciphertext, key, iv)
        return plaintext

    def screencap(self, num):
        if os.path.exists('C:\\screencap') != True:
            os.makedirs('C:\\screencap')

        screencap_path = f'/sdcard/screencap{num}.png'
        subprocess.Popen(f'adb shell screencap -p {screencap_path}', stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        time.sleep(1.8)
        subprocess.Popen(f'adb pull {screencap_path} C:\\screencap', stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    import re

    def has_chinese(self, string):
        pattern = re.compile(r'[\一-\龥]')
        match = pattern.search(string)
        return match is not None

    def install_source(self, str, path):
        if str == '直接':
            os.system(f'adb install {path}')
        elif str == '华为商店':
            os.system(f'adb install -i com.huawei.appmarket {path}')

    def moni_battery(self, num):
        cmd = f'adb shell dumpsys battery set level {num}'
        os.system(cmd)

    def get_luj(self, position, name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, position, name)
        return path

    def resource_path(self,relative_path):
        """获取程序中所需文件资源的绝对路径"""
        try:
            # PyInstaller创建临时文件夹,将路径存储于_MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
tool = Tool()


class QEventHandler(QtCore.QObject):
    def eventFilter(self, obj, event):
        """
        目前已经实现将拖到控件上文件的路径设置为控件的显示文本；
        """
        if event.type() == QtCore.QEvent.DragEnter:
            event.accept()
        if event.type() == QtCore.QEvent.Drop:
            md = event.mimeData()
            if md.hasUrls():
                # 此处md.urls()的返回值为拖入文件的file路径列表，支持多文件同时拖入；默认读取第一个文件的路径进行处理
                url = md.urls()[0]
                obj.setText(url.toLocalFile())
                # print(str(url.toLocalFile()))
                # print(type(url))
                return True
        return super().eventFilter(obj, event)


class MouseFilter(QtCore.QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.dragging = False
        self.drag_position = None

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - obj.frameGeometry().topLeft()
            return True
        elif event.type() == QEvent.MouseMove and self.dragging:
            obj.move(event.globalPos() - self.drag_position)
            return True
        elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            self.dragging = False
            self.drag_position = None
            return True
        else:
            return super().eventFilter(obj, event)
# if __name__ == '__main__':
