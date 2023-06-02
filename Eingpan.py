from aotudriver.aotudrivepy import AotuDriver
from aotudriver.get_info import GetInfo


class activiting:
    def __init__(self, device):
        self.get = GetInfo()
        self.device = device
        self.base = AotuDriver(device=self.device)

    def get_fullphonepath(self, apppath1):
        phone_files = rf"/sdcard/Android/data/{self.get.get_appPackagename(apppath1)}/cache/"
        return phone_files

    def install_and_debug(self, apppath1, debugpath1):
        try:
            self.base.app_install(apppath1)
            self.base.Sending_files_from_your_phone(debugpath1, self.get_fullphonepath(apppath1))
        except RuntimeError:
            return '安装超时请重试'
        return 'debug安装完成'
