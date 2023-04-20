# coding = utf-8
import json
import time
import logging

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)


class BasePage:
    """
    定义一个抽象类
    """

    # def __new__(cls, *args, **kwargs):
    #     if cls.__name__ == "BasePage":
    #         assert 0, "抽象类不能实例化"
    #     else:
    #         return super().__new__(*args, **kwargs)

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.maximize_window()

    def wait(self, func):
        """
        隐式等待
        :param driver:
        :param func:
        :return:
        """
        return WebDriverWait(self.driver, 10).until(func)

    def find_element(self, by=By.ID, value: str = None, need_text=False):
        """
        定位元素
        :param need_text: 是否需要文本
        :param by:
        :param value:
        :return:
        """

        def func(driver):
            text = self.driver.find_element(by, value).text

            if need_text:
                return text.replace(" ", "")
            else:
                return True

        self.wait(func)
        return self.driver.find_element(by, value)


class LoginPage(BasePage):
    ipt_username = (By.XPATH, '//*[@id="custom-validation_username"]')
    ipt_password = (By.XPATH, '//*[@id="custom-validation_password"]')
    login_button = (By.XPATH, '//*[@id="app"]/div/div/div[2]/form/div[3]/div/div/div/button/span')
    login_success = (By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')

    def login(self, username, password):
        """
        登录方法
        :param username: 用户名
        :param password: 密码
        :return:
        """
        self.driver.get("http://121.37.190.62:9200/login")
        time.sleep(3)
        self.driver.find_element(*self.ipt_username).send_keys(username)
        self.driver.find_element(*self.ipt_password).send_keys(password)
        self.driver.find_element(*self.login_button).click()

        # 判断是否登录成功
        if self.wait():
            print("登录成功")

            cookies = self.driver.get_cookies()
            with open("data/admin_cookie.json", "w") as f:
                for cookie in cookies:
                    f.write(json.dumps(cookie))

    def wait(self):
        wait = WebDriverWait(self.driver, 10)  # 手动设置等待对象

        def f(driver):
            text = self.driver.find_element(*self.login_success).text  # 定位文本进行判断
            if text:
                return text
            else:
                return False

        try:
            wait.until(f)
        except (TimeoutException, NoSuchElementException):
            logger.info("元素查找失败")

        return f(driver=self.driver)
