import time

from unittse.tools.get_driver import GetDriver
from unittse import page
from unittse.page.page_in import PageIn

class TestMpLogin:
    # 初始化
    def setup_class(self):
        # 获取驱动
        driver = GetDriver.get_wed_driver(page.url_mp)
        # 通过统一入口类获取PgaeMpLogin对象
        self.mp = PageIn(driver).page_get_PgaeMpLogin()

    # 结束
    def teardown_class(self):
        GetDriver.quit_web_driver()

    # 测试业务方法
    def test_mp_login(self, username='panhd', password='panhd0319'):

        # 调用登录业务方法
        self.mp.page_mp_login('panhd', 'panhd0319')

a = TestMpLogin()
a.setup_class()
a.test_mp_login()
a.teardown_class()