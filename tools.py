from pyaxmlparser import APK


def get_packname2(path):
    apk = APK(path)
    # 获取包名
    package_name = apk.package
    return str(package_name)


