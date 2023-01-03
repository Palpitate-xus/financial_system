import numpy as np
import akshare as ak
import show
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
def findrf():
    return ak.bond_zh_us_rate().values[-1][2] / 100

if __name__=='__main__':
    show.service.main.mainloop()