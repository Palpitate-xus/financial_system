import numpy as np
import akshare as ak
import jieba

# 获取无风险收益率
def findrf():
    return ak.bond_zh_us_rate().values[-1][2] / 100

# 获取股票数据
def fetchData(code='sz399552'):
    field_name = ak.stock_individual_info_em(symbol=code[2:8]).values[2][1]
    stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=code)
    data = []
    for item in stock_zh_index_daily_df.values:
        print((item[4]-item[1]) / item[1])
        data.append((item[4] - item[1]) / item[1])  # 求日收益率
    return data, field_name

# 求余弦相似度
def rept(s0,s1):
    vec = {}
    len0 = len1 = dotp =0
    for word in jieba.cut(s0):
        if(word in vec):
            vec[word][0] += 1
        else:
            vec[word] = [1,0]
    for word in jieba.cut(s1):
        if(word in vec):
            vec[word][1] += 1
        else:
            vec[word] = [0,1]
    for dim in vec:
        dotp += vec[dim][1] * vec[dim][0]
        len0 += vec[dim][0] ** 2
        len1 += vec[dim][1] ** 2
    return np.arccos(dotp / (np.sqrt(len0 * len1))) * 180 / np.pi

# 求解最优投资组合和行业重合度
def find(rf,list,namelist):
    l = len(list)
    if l <= 0: return
    er = np.array([np.average(i) for i in list])
    cov = np.cov(np.array(list), bias=True)
    w = np.array([1.0 for i in list])
    sharp = (np.sum(w * er) - rf * np.sum(w)) / np.sqrt(w.T.dot(cov).dot(w))
    for i in range(l):
        T = 2023.0
        while T>1e-14:
            pos = np.random.randint(0,l)
            dw = np.random.uniform(-w[pos],T)
            w[pos] += dw
            nsharp = (np.sum(w * er) - rf * np.sum(w)) / np.sqrt(w.T.dot(cov).dot(w))
            if nsharp > sharp:
                otc = w / np.sum(w)
                sharp = nsharp
            elif np.exp((nsharp - sharp) / T) < np.random.random():
                w[pos] -= dw
            T *= 0.993
    rep = np.array([[rept(namelist[i], namelist[j]) for i in range(l)] for j in range(l)])
    cov = np.array([[cov[i][j] * otc[i] * otc[j] for i in range(l)] for j in range(l)])
    return otc, sharp, np.sum(rep * cov) / np.sum(cov)

print(find(findrf(), [[0.02, 0.03],[0.04, 0.05]], ['test', 'new']))
print(fetchData()[1])
