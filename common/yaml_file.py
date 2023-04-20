# coding = utf-8

"""
自动读取yaml文件内容
"""
import yaml


class YamlFile(dict):
    def __init__(self, path):
        super().__init__()
        self._path = path
        self.load()

    def load(self):
        """
        加载yaml文件内容
        :return:
        """
        with open(self._path, mode="r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data:
                self.update(data)

    def save(self):
        with open(self._path, mode="w", encoding="utf-8")as f:
            yaml.dump(dict(self), f, allow_unicode=True)

