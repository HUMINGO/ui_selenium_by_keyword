# coding = utf-8
import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
from common.setting import *
from selenium.webdriver.support.select import Select
from common.driver import get_driver
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)


class KeyWord:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.maximize_window()

    def sleep(self, num, *args):
        time.sleep(num)

    def element_is_visible(self, loc: str, timeout=10, *args):
        """
        等待某个元素可见
        :param timeout: 超时时间
        :param loc: 元素定位
        :return:
        """
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((selenium_by, loc)))
            return True
        except TimeoutException:
            return False

    def open(self, url: str):
        """
        打开网址
        :param url:
        :return:
        """
        self.driver.get(url)

    def input_text(self, loc: str, text: str):
        """
        往输入框中输入内容
        :param loc:
        :param text:
        :return:
        """
        if self.element_is_visible(loc):
            self.find_element(selenium_by, loc).send_keys(text)
        else:
            raise Exception("元素定位失败")

    def click(self, loc: str):
        """
        点击操作
        :param loc:
        :return:
        """
        el = self.find_element(selenium_by, loc)
        el.click()

    def wait(self, func, *args):
        # 允许任意数量的参数
        return WebDriverWait(self.driver, wait_max_time).until(func)  # 等待 0~5秒

    def find_element(self, by, value, need_text=False, *args):
        """
        定位元素
        :param by:
        :param value:
        :param need_text:
        :param args:
        :return:
        """

        def f(driver, *args):  # 自定义
            txt = driver.find_element(by, value).text

            if need_text:  # 如果需要文本
                return txt.replace(" ", "")  # 返回文本进行判断
            else:  # 如果不需要文本
                return True  # 直接成功

        self.wait(f)  # 显式等待

        return self.driver.find_element(by, value)  # 返回元素

    def get_text(self, loc: str, need_text=True, *args):
        """
        获取文本
        :param loc: 定位
        :param need_text:
        :param args:
        :return:
        """

        def f(x, *args):
            e = self.driver.find_element(selenium_by, loc)
            t = e.text.replace(" ", "")
            if t:  # 文本是否包含非空字符串
                return t
            else:
                return False

        if need_text:  # 必须要有内容
            text = self.wait(f)
        else:
            text = self.find_element(selenium_by, loc).text

        return text

    def assert_equal(self, loc: str, assert_text, *args):
        """
        断言相等
        :param assert_text: 断言文本
        :param loc:
        :return:
        """
        element_text = self.get_text(loc)
        assert element_text == assert_text

    def iframe_enter(self, loc: str, *args):
        """
        进入iframe框架
        :param loc:
        :param args:
        :return:
        """
        element = self.find_element(selenium_by, loc)
        self.driver.switch_to.frame(element)

    def iframe_exit(self, *args):
        """
        退出iframe框架
        :param args:
        :return:
        """
        self.driver.switch_to.default_content()

    def clear(self, loc: str, *args):
        """
        清除输入框的内容
        :param loc:
        :param args:
        :return:
        """
        ele = self.find_element(selenium_by, loc)
        ele.clear()

    def select(self, loc: str, text: str, *args):
        """
        选择下拉选择框的内容
        :param text: 提示文本
        :param loc: 定位
        :param args:
        :return:
        """
        select = Select(self.find_element(selenium_by, loc))
        select.select_by_visible_text(text)

    def js(self, loc: str, code, *args):
        """
        执行js代码
        :param loc:
        :param code: js代码
        :param args:
        :return:
        """
        ele = self.find_element(selenium_by, loc)
        self.driver.execute_script(code, ele)

    def swipe(self, loc: str):
        """
        滑动到指定的元素位置
        :return:
        """
        ele = self.find_element(selenium_by, loc)
        while True:
            self.driver.execute_script('arguments[0].scrollIntoView(true);', ele)
            if self.element_is_visible(loc):
                break


if __name__ == '__main__':
    kw = KeyWord(get_driver())
    kw.open("https://www.sohu.com/")
    kw.swipe("/html/body/div[3]/div[5]/div[1]/div[1]/ul/li[1]/a")
    kw.sleep(5)
