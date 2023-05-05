import re
import subprocess
from PySide2 import QtCore
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import requests
from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import  QMainWindow

class Tool:
    # aab和签名文件是否匹配
    def get_keystoreSha(self, key_path, pwd):
        content = subprocess.Popen(f'keytool -list -v -keystore {key_path} -storepass {pwd}', stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out = content.communicate()[0].decode('gbk')
        p = re.compile('(?<=SHA1:).+')
        p2 = re.compile('(?<=SHA256:).+')
        p3 = re.compile('(?<=MD5:).+')
        key_Sha1 = p.findall(str(out))[0].strip()
        key_Sha256 = p2.findall(str(out))[0].strip()
        key_MD5 = p3.findall(str(out))[0].strip()
        return key_Sha1, key_Sha256, key_MD5

    def get_aabkeystoreSha(self, aab_path):
        content = subprocess.Popen(f'keytool -printcert -jarfile {aab_path}', stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out = content.communicate()[0].decode('gbk')

        p = re.compile('(?<=SHA1:).+')
        p2 = re.compile('(?<=SHA256:).+')
        p3 = re.compile('(?<=MD5:).+')

        aab_Sha1 = p.findall(str(out))[0].strip()
        aab_Sha256 = p2.findall(str(out))[0].strip()
        aab_MD5 = p3.findall(str(out))[0].strip()
        return aab_Sha1, aab_Sha256, aab_MD5

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





class CustomMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._mouse_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_dragging:
            self.move(self.pos() + (event.pos() - self._mouse_pos))

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            self._mouse_pos = None


if __name__ == '__main__':
    url = 'https://s.suitwallland.com/appCfg/v38?value=YW5kSWQ9MzFkOWE5ZWRkOGZmOWYyOSZhcHBpZD0zODY2NiZjaGE9Z29vZ2xlJmxzbj0yNDI5NDU2MDImcGxhdGZvcm09YW5kcm9pZCZwcmppZD0zODY2NjAyNiZ0aW1lc3RhbXA9MTY4MzE3MjUyNjU4OSZzaWduPTkxYmM1OWZhYzJmZDU4YjZhYzkzNTJmMzNlNzdlYTU0JmlzRGVidWc9MQ%3D%3D'
    pwd = 'dn123123'
    # path = r"C:/Users/zhangxy/Desktop/1/overtest.keystore"
    path1 = r'"C:\Users\zhangxy\Desktop\1\39254000.aab"'
    # tool.get_keystoreSha(path, pwd)
    print(tool.get_aabkeystoreSha(path1))
