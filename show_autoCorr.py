# -*- coding: utf-8 -*-
##### 自己相関 #####

import numpy as np
import matplotlib.pyplot as plt
import wavRead
import analTemp

wavFile = "＜分析したいオーディオデータ（のパス）＞.wav"
x, fs = wavRead.wav2int(wavFile)
t_dul = (len(x)-1)/fs
t = np.linspace(0, t_dul, len(x))

# 分析時刻（窓の中心）[s]
t_anal = 1.0

# 分析窓長 [s]
winSec = 100 * (10 ** -3)

# 分析対象の中心サンプル点
p_anal = round(fs * t_anal)

# 窓の総サンプル数
winSize = round(fs * winSec)
if winSize % 2 == 1:
  winSize = winSize + 1

# 分析区間の切り出し
i_ini = round(p_anal - winSize / 2)
i_fin = round(p_anal + winSize / 2)
xw = x[i_ini : i_fin]

# 分析区間の総パワー
den = np.sum(xw**2)

# 自己相関
r = analTemp.corrAuto(xw)
r = r / den

t = np.linspace(0, 1000*(winSize - 1)/fs, winSize)
Corr = r[0 : len(t)]

# プロット
plt.plot(t, Corr)
plt.xlabel("Time [ms]")
plt.ylabel("Autocorrelation value")
plt.xlim([0,t[-1]])
plt.ylim([-1, 1])

plt.show()
