# coding = utf-8
import pytest

from common.key_word import KeyWord
from common.driver import get_driver
import logging

logger = logging.getLogger(__name__)


# kw = KeyWord(get_driver())

def atest_login():
    kw = KeyWord(get_driver())
    logger.info("开始测试登录页面")
    kw.open("http://121.37.190.62:9200/login")
    kw.input_text('//*[@id="custom-validation_username"]', 'admin')
    kw.input_text('//*[@id="custom-validation_password"]', 'onesports')
    kw.click('//*[@id="app"]/div/div/div[2]/form/div[3]/div/div/div/button')
    kw.assert_equal('/html/body/div[2]/div/div/div/div/div/span[2]', '登录成功')
    kw.sleep(3)


@pytest.mark.parametrize("n", [1, 2, 4])
def btest_demo(n):
    print(n)
