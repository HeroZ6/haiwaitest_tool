import time

from unittse.base.base import Base
from unittse import page
class PageMpLoing_baidu(Base):
    # 输入用户名
    def page_input(self, value):
        self.base_input(page.chaxun, value)

    # 点击百度
    def page_ckick_baidu(self):
        a = self.baes_find(page.dianji)
        self.base_click(a)

    # 登陆页面组合业务方法
    def page_mp_chaxun(self, value):
        """
        提示：一般是同页面的操作
        """
        self.base_input(page.chaxun, value)
        time.sleep(1)
        self.base_click(page.dianji)
