import datetime
import os
import re
import subprocess



class GetInfo:

    def __init__(self):
        pass

    # 获取手机设备列表
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

    # 获得当前时间
    def get_current_timeH(self):
        return datetime.datetime.now().strftime('%H时%M分')
    def get_current_timeHM(self):
        return datetime.datetime.now().strftime('%H时%M分%S秒')
    def get_current_timeYMD(self):
        return datetime.datetime.now().strftime('%Y年%m月%d日')

    # 在指定目录下根据当前年月日创建一个文件夹，在根据当前时间创建一个文件并返回路径
    def full_save_folder(self, path):
        folder_YTD = self.create_folder_YTD(path)
        return fr'{self.create_folder_HMS(folder_YTD)}'
    # 在指定目录下根据当前年月日创建一个文件夹并返回绝对路径
    # 在指定目录下根据当前年月日创建一个文件夹并返回绝对路径
    def create_folder_HMS(self, path):
        """
        在指定目录下根据当前年月日创建一个文件夹，如果有了这个这个文件夹将不在创建
        :param path1:
        :param path5:
        :param pathname: 绝对路径
        :return: 返回已经创建完成文件夹的绝对路径
        """
        timename = datetime.datetime.now().strftime('%H时%M分%S秒')
        if timename in self.get_dirs_name(path):
            folderName = fr'{path}\{timename}'
            return folderName
        else:
            folderName = fr'{path}\{timename}'
            os.makedirs(folderName)
            return folderName

    def create_folder_YTD(self, path):
        """
        在指定目录下根据当前年月日创建一个文件夹，如果有了这个这个文件夹将不在创建
        :param path1:
        :param path5:
        :param pathname: 绝对路径
        :return: 返回已经创建完成文件夹的绝对路径
        """
        timename = datetime.datetime.now().strftime('%Y年%m月%d日')
        if timename in self.get_dirs_name(path):
            folderName = fr'{path}\{timename}'
            return folderName
        else:
            folderName = fr'{path}\{timename}'
            os.makedirs(folderName)
            return folderName

    #   得到一个路径下所有的[文件夹名称]
    def get_dirs_name(self, filepath):
        """
        得到一个路径下所有的[文件夹名称]
        :param filepath:绝对路径
        :return:
        """
        for root, dirs, files in os.walk(filepath):
            # print(root) #当前目录路径
            # print(dirs) #当前路径下所有子目录
            # print(files) #当前路径下所有非目录子文件
            return dirs

    def get_files_name(self, filepath):
        """
        得到一个路径下所有的[文件夹名称]
        :param filepath:绝对路径
        :return:
        """
        for root, dirs, files in os.walk(filepath):
            # print(root) #当前目录路径
            # print(dirs) #当前路径下所有子目录
            # print(files) #当前路径下所有非目录子文件
            return files
        #   得到一个路径下所有的[文件夹名称]

    def get_dirs_ptha(self, filepath):
        """
        得到一个路径下所有的[文件夹名称]
        :param filepath:绝对路径
        :return:
        """
        for root, dirs, files in os.walk(filepath):
            path = fr'{filepath}\{files}'
            return path

    #  得到一个路径下可读的包信息，包名作为主键，返回一个字典{包名：文件名}
    def get_easy_to_readAppInof(self, path):
        """
        :param path: 传入包的路径
        :return: 返回一个字典{项目id：[文件名]}
        """
        sqlit_file_name = []
        appinfo_dict = {}
        Packagename_list = self.get_Packagename_list(path)
        file_name_list = self.get_file_name(path, is_Removesuffix=False)
        file_name_list = list(file_name_list)
        indexv = 0
        for file_name in file_name_list:
            sqlit_file_name.append(file_name.split('_'))
            new_sqlit_file_name = sqlit_file_name[indexv]
            new_sqlit_file_name.append(file_name)
            indexv += 1

        for index in range(len(Packagename_list)):
            # 包名是主键
            # appinfo_dict[Packagename_list[index]] = sqlit_file_name[index]
            appinfo_dict[sqlit_file_name[index][0]] = sqlit_file_name[index]
        # print('>?>>',appinfo_dict)
        return appinfo_dict

        #  得到一个路径下可读的包信息，包名作为主键，返回一个字典{包名：文件名}

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

    def get_packagename_and_filename(self, path):
        """
        :param path: 传入包的路径
        :return: 返回一个字典{包名：[文件名]}
        """
        appinfo_dict = {}
        Packagename_list = self.get_Packagename_list(path)
        file_name_list = self.get_file_name(path, is_Removesuffix=False)
        file_name_list = list(file_name_list)
        for index in range(len(Packagename_list)):
            appinfo_dict[Packagename_list[index]] = file_name_list[index]
        return appinfo_dict

    # 获取指定路径下指定文件名称的包名
    def get_portion_Packagename_list(self, path, file_name_list):
        appPackageNames = []
        for file_name in file_name_list:
            full_path = rf'{path}\{file_name}'
            appPackageName = self.get_appPackagename(full_path)
            appPackageNames.append(appPackageName)
        return appPackageNames

    # 得到一个路径下所有安装包的包名反编译
    def get_Packagename_list(self, path):
        appPackageNames = []
        file_name_list = self.get_file_name(file_path=path, is_Removesuffix=False)
        for file_name in file_name_list:
            full_path = rf'{path}\{file_name}'
            # print(full_path)
            appPackageName = self.get_appPackagename(full_path)
            appPackageNames.append(appPackageName)
        return appPackageNames


    # 获取包名
    def get_appPackagename(self, path):
        """
        :param path: 包的绝对路径，反编译包得到包的包名
        :return:
        """
        cmd = "aapt dump badging %s" % path
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output.decode())
        if not match:
            return "获取不到包名,请检查apk路径是否有中文"
        appPackage = match.group(1)
        return appPackage


    # 获取文件名
    def get_file_name(self, file_path: object, is_Removesuffix: object = True) -> object:
        """
        :rtype: object
        :param file_path: 文件的绝对路径
        :param is_Removesuffix: 默认为：True，为True则去除文件名称后四位，为False则是完整的文件名称
        :return:返回 列表，路径下所有的文件名称
        """
        file_list = []
        for root, dirs, files in os.walk(file_path, topdown=False):
            if is_Removesuffix:
                for file in files:
                    file = list(file)
                    # 去除倒数四个值
                    file.pop(-1), file.pop(-1), file.pop(-1), file.pop(-1)
                    # print(i)
                    file = ''.join(file)
                    # print(f'为啥有桌面{file}')
                    # 如果名字是桌面就不保存，不是才保存
                    if file == 'desktop.ini':
                        files.remove('desktop.ini')
                    elif file == 'desktop':
                        print('desktop')
                        # files.remove('desktop')
                    else:
                        file_list.append(file)
                return file_list
            else:
                for file in files:
                    if file == 'desktop.ini':
                        files.remove('desktop.ini')
                    elif file == 'desktop':
                        files.remove('desktop')
                return files

        # 得到与电脑连接设备第一个的序列号

    # 获取一个序列号
    def get_deviceids(self):
        """
        得到与电脑连接设备第一个的序列号
        :return: 返回与电脑连接设备第一个的序列号
        """
        device = os.popen("adb devices").readlines()
        device_id = device[1]
        deviceID = device_id.split()
        return deviceID[0]

    # 传入一个整数，返回一个1-X的列表
    def get_Digital_list(self, num):
        """
        :param num：传入一个整数，返回一个1-X的列表
        :return:返回一个1-X的列表
        """
        rows_num_list = []
        for i in range(num):
            i += 1
            rows_num_list.append(i)
        return rows_num_list






