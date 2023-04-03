from selenium import webdriver

class GetDriver:
    # 1.声明变量
    __web_driver = None

    # 2.获取driver方法
    @classmethod
    def get_wed_driver(cls, url):
        if cls.__web_driver is None:
            # 获取web驱动
            cls.__web_driver = webdriver.Chrome()
            cls.__web_driver.get(url)
            cls.__web_driver.maximize_window()
        return cls.__web_driver

    # 退出driver方法
    @classmethod
    def quit_web_driver(cls):
        # 判断driver不为空时可以退出
        if cls.__web_driver:
            cls.__web_driver.quit()
            # 置空操作 重点： 我们执行结束quit方法后 我们driver退出了，但是driver在内存中的地址没有清空
            cls.__web_driver = None