from selenium.webdriver.common.by import By

"""以下数据为自媒体、后台管理url"""
url_mp = 'https://www.baidu.com'






"""以下数据为配置信息"""
# 元素
mp_username = (By.CSS_SELECTOR,'[placeholder="请输入账号"]')
mp_password = (By.CSS_SELECTOR,'[placeholder="请输入密码"]')
mp_login = (By.CSS_SELECTOR,'.el-button el-button--Xprimary el-button--small')
mp_nickname = (By.CSS_SELECTOR,'.el-icon-user-solid')

# 百度元素
chaxun = (By.ID, 'kw')
dianji = (By.ID, 'su')




