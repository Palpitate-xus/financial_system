import numpy as np
import akshare as ak
import jieba
import math
import re
import time

# 获取无风险收益率
def findrf():
    return ak.bond_zh_us_rate().values[-1][2] / 100

# 求余弦相似度
def rept(s0,s1):
    vec={}
    len0=len1=dotp=0
    for word in jieba.cut(s0):
        if(word in vec):
            vec[word][0]+=1
        else:
            vec[word]=[1,0]
    for word in jieba.cut(s1):
        if(word in vec):
            vec[word][1]+=1
        else:
            vec[word]=[0,1]
    for dim in vec:
        dotp+=vec[dim][1]*vec[dim][0]
        len0+=vec[dim][0]**2
        len1+=vec[dim][1]**2
    return math.acos(dotp/(math.sqrt(len0*len1)))*180/math.pi