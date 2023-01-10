import tkinter as tk
from tkinter import filedialog,messagebox
import tool
otc=''
class service():
    def confirm():
        datalist,namelist,minlen=[],[],800
        try:
            for code in service.exch.get(0.1,'end').split():
                tem=tool.fetchData(code)
                datalist.append(tem[0])
                namelist.append(tem[1])
            if not datalist:exit(0)
        except:
            messagebox.showerror(title='Error',message='error input')
            return
        minlen=min(len(item) for item in datalist)
        if minlen<36:
            messagebox.showinfo(title='info',message='too less sample was found')
            return
        datalist=list(map(lambda x:x[:minlen],datalist))
        try:
            ans=tool.find(tool.findrf(),datalist,namelist)
        except:
            messagebox.showerror(title='Error',message='unknown calculation error')
            return
        global otc
        otc='SharpRatio='+str(ans[1])+'\n'+'dispersity='+str(ans[2])+'\n'
        for w in ans[0]:
            otc+=str(w)+'\n'
        solve().main.focus()
    def readfile():
        path=filedialog.askopenfilename()
        try:xx=open(path,'r')
        except:return
        service.exch.delete(0.1,'end')
        codes=''
        for line in xx.readlines():
            codes+=line
        service.exch.insert(0.1,codes)
        xx.close()
    def cancel():
        service.main.destroy()
    main=tk.Tk()
    main.title('模拟退火求最优风险组合')
    main.resizable(0,0)
    main.geometry('640x420+500+200')
    exch=tk.Text(main,font=('times',12),wrap='char')
    exch.place(x=15,y=30,width=440,height=250)
    tk.Label(main,font=('times',12),justify='left',text='输入股票代码\n\n用换行或空格隔开').place(x=480,y=30,width=140,height=90)
    sc=tk.Scrollbar(main,command=exch.yview)
    sc.place(x=455,y=30,width=15,height=250)
    exch.config(yscrollcommand=sc.set)
    tk.Button(main,font=('times',12),text='确定',command=confirm).place(x=480,y=220,width=150,height=60)
    tk.Button(main,font=('times',12),text='退出',command=cancel).place(x=480,y=320,width=150,height=60)
    tk.Label(main,font=('times',12),anchor='w',text='或者您可以读入文本文件').place(x=15,y=310,width=400,height=30)
    tk.Button(main,font=('times',10),text='选择文件',command=readfile).place(x=15,y=350,width=60,height=30)
class solve():
    def __init__(self):
        def confirm():
            self.main.destroy()
        def savefile():
            path=filedialog.asksaveasfilename()
            xx=open(path,'a+')
            xx.write(otc)
            xx.close()
        self.main=tk.Toplevel()
        self.main.title('计算结果')
        self.main.resizable(0,0)
        self.main.geometry('480x640+500+100')
        show=tk.Text(self.main,font=('times',12))
        show.place(x=0,y=0,width=480,height=560)
        sc=tk.Scrollbar(show,command=show.yview)
        sc.pack(side='right',fill='y')
        show.insert(0.1,otc)
        show.config(state='disabled',yscrollcommand=sc.set)
        tk.Button(self.main,font=('times',12),text='确定',command=confirm).place(x=120,y=585,width=50,height=30)
        tk.Button(self.main,font=('times',12),text='保存到文件',command=savefile).place(x=270,y=585,width=100,height=30)
if __name__=='__main__':
    service().main.mainloop()
'''
sh000001
sh688011
sh688071
sh688280
sh688258
sh600476
sh600870
sh600283
'''