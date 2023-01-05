import numpy as np
import akshare as ak


# 获取无风险收益率
def findrf():
    return ak.bond_zh_us_rate().values[-1][2] / 100