#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: excel.py
@Desc: None
"""
import xlrd
import xlwt


class Excel(object):
    styleHead = None
    sheet = None
    excel = None

    def __init__(self, header: [], data: [], path: str, sheet: str):
        self.header = header
        self.data = data
        self.sheet = sheet
        self.path = path

        self.__initExcel()

    def __initExcel(self):
        self.styleHead = xlwt.XFStyle()
        font = xlwt.Font()  # 初始化字体相关
        font.name = "微软雅黑"
        font.bold = True
        font.colour_index = 1  # TODO 必须是数字索引
        # 初始背景图案
        bg = xlwt.Pattern()
        # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        bg.pattern = xlwt.Pattern.SOLID_PATTERN
        # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan,
        # 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown),
        # 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
        bg.pattern_fore_colour = 4

        # 设置字体
        self.styleHead.font = font
        # 设置背景
        self.styleHead.pattern = bg

        self.excel = xlwt.Workbook()
        # 添加工作区
        self.sheet = self.excel.add_sheet(self.sheet)

    def create(self):
        # create excel header.
        for index, val in enumerate(self.header):
            self.sheet.write(0, index, val, self.styleHead)

        for index, valList in enumerate(self.data, 1):
            for i, key in enumerate(valList):
                self.sheet.write(index, i, valList[key])

        self.excel.save(self.path)

    def get(self, path: str):
        return xlrd.open_workbook(path)
