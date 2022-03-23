#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: main.py
@Desc: None
"""
import sys

sys.path.append("../src")

from matplotlib import pyplot as plt
from src.futures import Futures
import pandas as pd


def example():
    # Fetch data, then generate excel.
    f = Futures("SC0")
    historyList = f.history("2010-01-01", "2022-03-23")
    df = pd.DataFrame(historyList)
    df.to_excel("./SC0.xlsx", sheet_name='Sheet1', engine='xlsxwriter')

    f = Futures("AU0")
    historyList = f.history("2010-01-01", "2022-03-23")
    df = pd.DataFrame(historyList)
    df.to_excel("./AU0.xlsx", sheet_name='Sheet1', engine='xlsxwriter')

    # Reade data，then generate line chart.
    au0Df = pd.read_excel("./AU0.xlsx")
    sc0Df = pd.read_excel("./SC0.xlsx")
    au0Df = pd.DataFrame(au0Df, columns=["date", "closingPrice"])
    sc0Df = pd.DataFrame(sc0Df, columns=["date", "closingPrice"])
    au0Df = au0Df.rename(columns={"closingPrice": "au0-price"})
    sc0Df = sc0Df.rename(columns={"closingPrice": "sc0-price"})
    concatList = sc0Df.merge(au0Df, on="date", how="left")

    concatList.plot(x="date",
                    y=["au0-price", "sc0-price"],
                    ylabel="price",
                    figsize=(300, 15),
                    xticks=(range(0, len(concatList))),
                    x_compat=True
                    )
    plt.xticks(rotation=90)

    # plt.show()
    plt.savefig("./res.png", format="png")


if __name__ == '__main__':
    example()
