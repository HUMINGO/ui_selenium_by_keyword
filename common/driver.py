# coding = utf-8

from selenium.webdriver import Chrome, Firefox, Ie, Safari, Edge
from common.setting import *


def get_driver(name: str = driver_type):
    """
    根据传入的关键字获取到对应的浏览器对象
    :param name:
    :return:
    """
    name = name.lower()
    name = name.replace(" ", "")
    if name == "chrome":
        return Chrome()
    elif name == "firefox":
        return Firefox()
    elif name == "ie":
        return Ie()
    elif name == "safari":
        return Safari()
    elif name == "edge":
        return Edge()
