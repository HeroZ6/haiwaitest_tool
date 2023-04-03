from unittse.page.baidu_mp_chaxun import PageMpLoing_baidu

class baidu_PageIn:
    """
    实例化驱动
    """
    def __init__(self,driver):
        self.driver = driver

    # 获取PageMpLogin对象
    def page_get_PgaeMpLogin(self):
        """
        将实例化的驱动传入 PageMpLoing中返回一个PageMpLoing对象
        """
        # 这里的是将驱动传入 page_mp_login文件中的PageMpLoing类，实例化成对象进行返回
        return PageMpLoing_baidu(self.driver)