# coding = utf-8

import openpyxl


class ExcelFile(dict):

    def __init__(self, path):
        super().__init__()
        self._path = path
        self.load()

    def load(self):
        # 打开工作表
        workbook = openpyxl.load_workbook(self._path)
        data = {}
        for sheet in workbook.worksheets:
            data[sheet.title] = []
            for row in sheet.iter_rows(values_only=True):
                data[sheet.title].append(row)

        if data:
            self.update(data)

