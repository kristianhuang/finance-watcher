#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: excel.py
@Desc: None
"""

import pandas as pd


def save(data: [], path: str):
    df = pd.DataFrame(data)
    df.to_excel(path, sheet_name='Sheet1', engine='xlsxwriter')


def read(path: str):
    return pd.read_excel(path)
