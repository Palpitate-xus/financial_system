import numpy as np
def find(rf,*list):
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
    return [otc,sharp]
print(find(0.02,(1,1,1,2),(2,3,4,5),(2,5,3,4)))
