# coding = utf-8
import json
import time

import pytest
import yaml
from selenium.webdriver import Chrome
from common.pom import LoginPage
from common.driver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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




@pytest.fixture(scope='session', autouse=True)
def get_token():
    """
    获取到localstorage
    :return:
    """
    driver = get_driver()
    driver.implicitly_wait(10)
    loginPage = LoginPage(driver)
    loginPage.login("humin", "20250909")
    # driver.find_element(By.XPATH, '//*[@id="app"]/section/aside/div/div/p')
    local_storage = driver.execute_script('return window.localStorage')
    print(local_storage)
    with open('data/admin_cookie.json', 'w') as f:
        f.write(json.dumps(local_storage))




@pytest.fixture
def auto_login_admin():
    """
    优先通过已保存的 Cookie 登录，Cookie 无效时使用账号密码登录。
    :return:
    """
    driver = get_driver()
    try:
        driver.get(base_url)

        try:
            with open('data/admin_cookie.json', encoding='utf-8') as f:
                cookies = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("读取登录 Cookie 失败，将使用账号密码登录: %s", exc)
            cookies = []

        # 兼容早期文件中只保存单个 Cookie 对象的格式。
        if isinstance(cookies, dict):
            cookies = [cookies]

        for cookie in cookies:
            cookie = dict(cookie)
            # Selenium 不接受从浏览器导出的 sameSite=None 字符串。
            if cookie.get('sameSite') not in ('Strict', 'Lax', 'None'):
                cookie.pop('sameSite', None)
            try:
                driver.add_cookie(cookie)
            except Exception as exc:
                logger.warning("跳过无法注入的 Cookie %r: %s", cookie.get('name'), exc)

        if cookies:
            driver.refresh()
            time.sleep(2)

        # 用应用内登录后的首页元素判断状态，给前端路由跳转留出时间。
        login_success = (By.XPATH, '//*[@id="root"]/div[1]/section/aside/div/div[1]/ul/li[1]/span/a/span/span[2]')
        logged_in = False
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(login_success))
            logged_in = True
        except Exception:
            logger.info("Cookie 未建立登录状态，改用账号密码登录")

        if not logged_in:
            LoginPage(driver).login("humin", "20250909")
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(login_success))
            except Exception as exc:
                raise RuntimeError(
                    "Cookie 登录和账号密码登录均未成功；请确认 Cookie 未过期，且登录账号可用。"
                ) from exc

        yield driver
    finally:
        driver.quit()


