#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: futures.py
@Desc: None
"""
import re

from bs4 import BeautifulSoup

from src.util import time, request


class Futures(object):
    baseUrl = "https://vip.stock.finance.sina.com.cn/"
    domTree = None

    # code: pz
    codeList = {"SC0": 13, "AU0": 7, "AG0": 8}

    def __init__(self, code: str):
        """

        :param code: Futures No，The code in (SC0, AU0, AG0).
        """
        self.code = code
        self.pz = self.codeList[code]

    def history(self, startTime, endTime):
        """ get gold price history list.

        :param startTime: Start time, e.g. 2020-02-01.
        :param endTime: End time, e.g. 2022-02-01.
        :return: history list
        """
        startTime = time.formatTime(startTime)
        endTime = time.formatTime(endTime)
        historyList = []
        url = self.baseUrl + f"/q/view/vFutures_History.php?&jys=1&pz={self.pz}&hy=0&breed={self.code}&start={startTime}&end={endTime}"
        self.__createDomTree(request.fetchData(url))
        page = self.__findPage()
        for p in range(page):
            url = self.baseUrl + f"q/view/vFutures_History.php?page={p + 1}&breed={self.code}&start={startTime}&end={endTime}&jys=1&pz={self.pz}&hy=0&name=%B4%F3%B6%B91109"
            self.__createDomTree(request.fetchData(url))
            self.__generateHistoryList(historyList)

        return historyList

    def __createDomTree(self, body: str):
        """生成 dom 树.

        :param body: html body.
        :return: None
        """
        self.domTree = BeautifulSoup(body, "lxml")

    def __findPage(self):
        """根据 dom 树查找数据的页码

        :return: 页码
        """
        page = 1
        res = self.domTree.find("td", class_="tdr", align="center")
        if res is None:
            return page
        pattern = re.findall(r'\d+', res.get_text(strip=True))

        return int(pattern[1])

    def __generateHistoryList(self, historyList):
        """查找并生成数据列表

        :return: 数据列表
        """
        historyListDom = self.domTree.find("div", class_="historyList").table.find_all("tr")
        for item in historyListDom[2:]:
            dataDom = item.find_all("div")
            itemData = {
                "date": dataDom[0].get_text(strip=True),
                "closingPrice": dataDom[1].get_text(strip=True),
                "openingPrice": dataDom[2].get_text(strip=True),
                "highestPrice": dataDom[3].get_text(strip=True),
                "lowestPrice": dataDom[4].get_text(strip=True),
                "volume": dataDom[5].get_text(strip=True)
            }

            historyList.append(itemData)

    def __generateInfo(self):
        table = self.domTree.find_all(id="list_nav2")
        print(table)
