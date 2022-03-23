#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: time.py
@Desc: None
"""

import time


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
