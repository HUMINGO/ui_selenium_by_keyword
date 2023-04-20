# coding = utf-8

"""
编写字符串模板方法，将测试用例yaml文件中的${}进行替换，包含热加载方法的执行
"""
import copy
import re
import string


def _str(s) -> str:
    return f"'{s}'"


class Template(string.Template):
    """
    功能：支持函数调用，参数也可以是变量
    """

    func_mapping = {
        "str": _str,
        "float": float,
        "bool": bool,
        "int": int,
        "open": open,
        "len": len
    }

    call_pattern = re.compile(r"\${(?P<func_name>.*?)\((?P<func_args>.*?)\)}")

    def render(self, mapping: dict) -> str:
        s = self.safe_substitute(mapping)  # 原有方法替换变量
        s = self.safe_substitute_funcs(s, mapping)  # 新方法替换函数结果

        return s

    def safe_substitute_funcs(self, template, mapping) -> str:
        """
        解析字符串中的函数名和参数，并调用函数，并将结果替换用例中的设置的参数变量（如${get_new_str(token)}）
        :param template: 字符串
        :param mapping: 上下文，提供要使用的函数和变量
        :return: 替换后的结果
        """

        mapping = copy.deepcopy(mapping)
        mapping.update(self.func_mapping)  # 合并两个mapping

        def convert(mo):
            func_name = mo.group("func_name")
            func_args = mo.group("func_args").split(",")

            func = mapping.get(func_name)  # 读取指定函数
            func_args_value = [mapping.get(arg, arg) for arg in func_args]

            if func_args_value == [""]:
                func_args_value = []

            if not callable(func):
                return mo.group()  # 如果是不可调用的假函数,不进行替换
            else:
                return str(func(*func_args_value))  # 否则用函数结果进行替换

        return self.call_pattern.sub(convert, template)


def hot_load():
    """
    函数热加载，将热加载函数添加到Template中的mapping中
    :return:
    """
    from common import hot_load_funcs

    for func_name in dir(hot_load_funcs):
        if func_name.startswith("_"):
            continue
        func_code = getattr(hot_load_funcs, func_name)
        if callable(func_code):
            Template.func_mapping[func_name] = func_code


hot_load()
