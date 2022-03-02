#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: gold.py
@Desc: None
"""
import re
import time

import requests
from bs4 import BeautifulSoup


def formatTime(timeData):
    """格式化时间字符串

    :param timeData: 时间字符串
    :return: 格式化后的时间字符串， "2022-03-01"
    """

    try:
        res = time.strptime(timeData, "%Y-%m-%d")
    except ValueError:
        raise ValueError("请输入正确的时间范围,例如 2022-02-01")

    return time.strftime("%Y-%m-%d", res)


class Gold(object):
    baseUrl = "https://vip.stock.finance.sina.com.cn/"
    logPath = ""
    domTree = None

    def history(self, startTime, endTime):
        startTime = formatTime(startTime)
        endTime = formatTime(endTime)
        historyList = []
        url = self.baseUrl + f"/q/view/vFutures_History.php?&jys=1&pz=7&hy=0&breed=AU0&start={startTime}&end={endTime}"
        self.__createDomTree(self.__fetchData(url))
        page = self.__findPage()
        for p in range(page):
            url = self.baseUrl + f"q/view/vFutures_History.php?page={p + 1}&breed=AU0&start={startTime}&end={endTime}&jys=shfe&pz=AU&hy=AU0&type=inner&name="
            self.__createDomTree(self.__fetchData(url))
            self.__generateHistoryData(historyList)

        return historyList

    def __genericHeader(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
        }

        return headers

    def __fetchData(self, url):
        """发送请求.

        :param url(str): 请求地址
        :param headers(dict, str): 请求头
        :return: 相应主体
        """
        self.__genericHeader()

        return requests.get(url=url, headers=self.__genericHeader()).text

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

    def __generateHistoryData(self, historyList):
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


g = Gold()
g.history("2021-02-01", "2022-03-02")
