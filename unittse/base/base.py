from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Base:
    # 初始化
    def __init__(self, driver):
        self.driver = driver

    def baes_find(self, loc, time=30, poll_frequency=0.5):
        '''
            封装查找方法
           loc = 元素类型,可以是一个列表或是元组
           time = 等待时间、默认30秒超时时间
           poll_frequency = 多久捕获一次页面元素，默认0.5秒
        '''
        self.driver.find_element
        return WebDriverWait(driver=self.driver, timeout=time, poll_frequency=poll_frequency).until(lambda x: x.find_element(*loc))

    def base_input(self, loc, value):
        """
           定义输入方法
            loc = 元素类型,可以是一个列表或是元组
           value = 输入的值
        """
        # 获取元素
        el = self.baes_find(loc)
        # 清空操作
        el.clear()
        # 输入值
        el.send_keys(value)

    #    点击元素
    def base_click(self, loc):
        """
        :param loc: 元素类型,可以是一个列表或是元组
        :return:
        """
        self.baes_find(loc).click()

    def base_get_txet(self,loc):
        """
         定义获取元素文本方法
            loc = 元素类型,可以是一个列表或是元组
           return = 返回一个元素的文本
        """
        return self.baes_find(loc).txet

