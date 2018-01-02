# -*- coding: utf-8 -*-


from tkinter import *
import numpy as np
import scipy.stats as sps


class Option:

    def __init__(self, cp, s0, k, t, r, sigma, dv=0):
        self.cp = 'Call' if (cp == 'C' or cp == 'c') else 'Put'
        self.cp_sign = 1.0 if self.cp == 'Call' else -1.0
        self.s0 = s0 * 1.0
        self.k = k * 1.0
        self.t = t * 1.0
        self.sigma = sigma * 1.0
        self.r = r * 1.0
        self.dv = dv * 1.0
        self.d_1 = (np.log(self.s0 / self.k) + (self.r - self.dv + .5 * self.sigma ** 2) * self.t) / self.sigma / np.sqrt(self.t)
        self.d_2 = self.d_1 - self.sigma * np.sqrt(self.t)

    def bsprice(self):
        return self.cp_sign * self.s0 * np.exp(-self.dv * self.t) * sps.norm.cdf(self.cp_sign * self.d_1) \
               - self.cp_sign * self.k * np.exp(-self.r * self.t) * sps.norm.cdf(self.cp_sign * self.d_2)

    def mcprice(self, iteration=1000000):
        zt = np.random.normal(0, 1, iteration)
        st = self.s0 * np.exp((self.r - self.dv - .5 * self.sigma ** 2) * self.t + self.sigma * self.t ** .5 * zt)
        p = []
        for St in st:
            p.append(max(self.cp_sign * (St - self.k), 0))
        return np.average(p) * np.exp(-self.r * self.t)

def calc():
    vlist = []
    for e in elist:
        try:
            p = float(e.get())
            vlist.append(p)
        except:
            answ.config(text='Invalid Input(s). Please input correct parameter(s)', fg='red')
            e.delete(0, len(e.get()))
            return 0

    for i in range(6):
        if i != 3 and vlist[i] < 0:
            answ.config(text='Invalid Input(s). Please input correct parameter(s)', fg='red')
            elist[i].delete(0, len(elist[i].get()))
            return 0

    vlist[6] = int(vlist[6])
    if vlist[6] < 1000:
        vlist[6] = 1000
        elist[6].delete(0, len(elist[6].get()))
        elist[6].insert(0, '1000')
    elif vlist[6] > 10000000:
        vlist[6] = 10000000
        elist[6].delete(0, len(elist[6].get()))
        elist[6].insert(0, '10000000')

    o = Option(cp.get(), vlist[0], vlist[1], vlist[2] / 365, vlist[3], vlist[4], vlist[5])
    answ.config(text='The result is as follows:', fg='black')
    bs.config(text=str("%.8f"%o.bsprice()))
    mc.config(text=str("%.8f"%o.mcprice(iteration=vlist[6])))


# construct a window, title it, and preface it.
root = Tk()
root.wm_title('European Option Price Calculator')
Label(root, text='Please input relevant parameters, '
                 'then click "Calculate" button.').grid(row=0, column=0, columnspan=3)
Label(root, text='by Johnny MOON, COB @UIUC').grid(columnspan=3)

# choose Call or Put option and store it in cp.
cp = StringVar()
Label(root, text='Option Type').grid(row=2, column=0, sticky=W)
Radiobutton(root, text='Call', variable=cp, value='c').grid(row=2, column=1)
Radiobutton(root, text='Put', variable=cp, value='p').grid(row=2, column=2)

# input different parameters
plist = ['Current Price', 'Strike Price', 'Days to Maturity',
         'Risk-free Rate', 'Volatility', 'Continuous Dividend Rate', 'MC Iteration']
elist = []
r = 3
for param in plist:
    Label(root, text=param).grid(column=0, sticky=W)
    e = Entry(root)
    e.grid(row=r, column=1, columnspan=2, sticky=W+E)
    elist.append(e)
    r += 1

# Calculate button
Button(root, text='Calculate', command=calc).grid(row=r)
r += 1
answ = Label(root, text='The result is as follows:')
answ.grid(row=r, columnspan=3)
r += 1
bs = Label(root)
mc = Label(root)
bs.grid(row=r, columnspan=2, sticky=E)
mc.grid(row=r+1, columnspan=2, sticky=E)
Label(root, text='Use BS formula: ').grid(row=r, sticky=W)
Label(root, text='Use Monte Carlo: ').grid(row=r+1, sticky=W)

root.mainloop()
