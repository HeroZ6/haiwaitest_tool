import time

from unittse.base.base import Base
from unittse import page
class PageMpLoing(Base):
    # 输入用户名
    def page_input_username(self, username):
        self.base_input(page.mp_username, username)

    # 输入密码
    def page_input_password(self, passwodr):
        self.base_input(page.mp_password, passwodr)

    # 点击登陆
    def page_ckick_login_btn(self):
        self.baes_find(page.mp_login)

    # 获取昵称
    def page_get_nickname(self):
        return self.base_get_txet(page.mp_nickname)

    # 登陆页面组合业务方法
    def page_mp_login(self, username, password):
        """
        提示：一般是同页面的操作
        """
        self.page_input_username(username)
        self.page_input_password(password)
        time.sleep(1)
        self.page_ckick_login_btn()

