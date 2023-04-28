import os
import re
import subprocess
from PySide2 import QtCore


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


if __name__ == '__main__':
    pwd = 'dn123123'
    # path = r"C:/Users/zhangxy/Desktop/1/overtest.keystore"
    path1 = r'"C:\Users\zhangxy\Desktop\1\39254000.aab"'
    # tool.get_keystoreSha(path, pwd)
    print(tool.get_aabkeystoreSha(path1))
