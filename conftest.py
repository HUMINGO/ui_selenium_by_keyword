# coding = utf-8
import json
import time

import pytest
import yaml
from selenium.webdriver import Chrome
from common.pom import LoginPage
from common.driver import get_driver
from selenium.webdriver.common.by import By
from pytest_xlsx.file import XlsxItem
import logging
from common.key_word import KeyWord
import allure
from common.templates import Template
from common.yaml_file import YamlFile
from common.utils import *
from common.setting import *

logger = logging.getLogger(__name__)


def pytest_xlsx_run_step(item: XlsxItem):
    """
    执行Excel用例的钩子函数
    :param item:
    :return:
    """
    driver_name = list(item.usefixtures.keys())[0]
    driver = item.usefixtures[driver_name]
    kw = KeyWord(driver)

    step = item.current_step  # 得到的是一个字典
    step_yaml_str = yaml.dump(step)
    s = Template(step_yaml_str).render(YamlFile(loc_yaml))
    step = yaml.safe_load(s)

    remark = step.pop("说明")
    key = step.pop("标记")
    params = list(step.values())

    if key is None:
        return

    params = get_list(params)
    logger.info(f"执行关键字：{key}，参数：{params}")

    func = getattr(kw, key)
    func(*params)

    png = driver.get_screenshot_as_png()  # 截图
    allure.attach(png, name=remark)


@pytest.fixture
def anonymous_driver():
    driver = get_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope='function', autouse=False)
def user_login_driver():
    driver = get_driver()
    loginPage = LoginPage(driver)
    loginPage.login("admin", "onesports")
    return driver


@pytest.fixture(scope='function', autouse=False)
def auto_login_with_cookies():
    """
    自动登录管理后台，通过cookie来管理登录
    :return:
    """
    # 1、判断是否登录
    driver = get_driver()
    driver.get("http://121.37.190.62:9200")
    driver.refresh()
    time.sleep(2)
    if driver.title == "登录":  # 未登录，加载cookies看是否能够成功登录
        with open('data/admin_cookie.json', mode='r') as f:
            _data = f.read()
            if _data:
                cookies = json.loads(f.read())
            else:
                cookies = []
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        if driver.title == "登录":
            loginPage = LoginPage(driver)
            loginPage.login("admin", "onesports")


def get_token():
    """
    获取到localstorage
    :return:
    """
    driver = get_driver()
    driver.implicitly_wait(10)
    loginPage = LoginPage(driver)
    loginPage.login("admin", "onesports")
    driver.find_element(By.XPATH, '//*[@id="app"]/section/aside/div/div/p')
    local_storage = driver.execute_script('return window.localStorage')
    print(local_storage)
    with open('local_storage.json', 'w') as f:
        f.write(json.dumps(local_storage))


def set_token():
    """
    设置local_storage
    :return:
    """
    driver = get_driver()
    driver.get("http://121.37.190.62:9200")

    with open('local_storage.json') as f:
        storage = json.loads(f.read())
        print(storage)

    for i in dict(storage).keys():
        if dict(storage)[i] is None:
            continue
        else:
            value = dict(storage)[i]
            driver.execute_script(f"window.localStorage.setItem('{i}', '{value}')")

    driver.refresh()
    input()


@pytest.fixture
def auto_login_admin():
    """
    自动登录
    :return:
    """
    driver = get_driver()
    driver.get("http://121.37.190.62:9200")
    time.sleep(3)
    # 判断是否登录
    if driver.title == "登录":  # 说明没有登录需要进行登录
        with open('local_storage.json') as f:
            storage = json.loads(f.read())
        if storage is None:  # 没有值就不能自动登录
            loginPage = LoginPage(driver)
            loginPage.login("admin", "onesports")
        else:
            for i in dict(storage).keys():
                if dict(storage)[i] is None:
                    continue
                else:
                    value = dict(storage)[i]
                    driver.execute_script(f"window.localStorage.setItem('{i}', '{value}')")

        driver.refresh()
    else:  # 说明已经登录了
        pass
    yield driver
    driver.quit()


if __name__ == '__main__':
    auto_login_admin()
