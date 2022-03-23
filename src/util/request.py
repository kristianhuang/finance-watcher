#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: request.py
@Desc: None
"""
import requests


def __genericHeader():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }

    return headers


def fetchData(url: str):
    """send request.

    :param url: request url
    :return: reps body
    """
    return requests.get(url=url, headers=__genericHeader()).text
