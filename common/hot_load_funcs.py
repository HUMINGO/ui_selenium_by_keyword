# coding = utf-8

"""
文件包含所有的热加载方法
"""
import random
import time


def get_timestamps():
    return time.time()


def generate_random_str():
    """
    生成一个指定长度的字符串
    """
    random_str = ''
    base_str = '91AAEB54-F66C-4710-A966-9DC9EDBC9CED'
    str_length = len(base_str) - 1
    for i in range(str_length):
        random_str += base_str[random.randint(0, str_length)]
    return random_str


def open_file(file_path):
    """
    打开文件
    :param file_path: 文件路径
    :return:
    """
    return open(file_path, mode="rb", encoding="utf-8")


def get_username():
    """
    获取用户名
    :return:
    """
    return "admin"


def get_password():
    """
    获取密码
    :return:
    """
    return "onesports"
