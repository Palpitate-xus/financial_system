import numpy as np
import akshare as ak
def find(rf,list):
    l=len(list)
    if l==0:return
    er=np.array([np.average(i) for i in list])
    cov=np.cov(np.array(list),bias=True)
    w=np.array([1.0 for i in list])
    sharp=(np.sum(w*er)-rf*np.sum(w))/np.sqrt(w.T.dot(cov).dot(w))
    for i in range(l):
        T=2023.0
        while T>1e-14:
            pos=np.random.randint(0,l)
            dw=np.random.uniform(-w[pos],T)
            w[pos]+=dw
            nsharp=(np.sum(w*er)-rf*np.sum(w))/np.sqrt(w.T.dot(cov).dot(w))
            if nsharp>sharp:
                otc=w/np.sum(w)
                sharp=nsharp
            elif np.exp((nsharp-sharp)/T)<np.random.random():
                w[pos]-=dw
            T*=0.993
    return otc,sharp

def fetchData(code='sz399552'):
    stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=code)
    data = []
    for item in stock_zh_index_daily_df.values:
        print((item[4]-item[1])/item[1])
        data.append((item[4]-item[1])/item[1])  # 求日收益率
    return data

data = []
length = []
codes = input().split()
for item in codes:
    temp = fetchData(item)
    data.append(temp)
    length.append(len(temp))
minlength = min(length)
for item in data:
    if len(item) > minlength:
        item = item[0:minlength]
rf = float(input('请输入无风险收益率:'))
print(find(rf,data))
