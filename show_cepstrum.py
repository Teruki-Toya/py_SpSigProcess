# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import wavRead
import analFreq

wavFile = "＜分析したいオーディオデータ（のパス）＞.wav"
x, fs = wavRead.wav2int(wavFile)
t_dul = (len(x)-1)/fs
t = np.linspace(0, t_dul, len(x))

# 分析時刻（窓の中心）[s]
t_anal = 2.0

# 分析窓長 [s]
winSec = 100 * (10 ** -3)

p_anal = round(fs * t_anal)
winSize = round(fs * winSec)

if winSize % 2 == 1:
  winSize = winSize + 1

i_ini = round(p_anal - winSize / 2)
i_fin = round(p_anal + winSize / 2)
xw = x[i_ini : i_fin]

xc = analFreq.cepstrum(xw, winSize)

quef = np.linspace(0, int(1000*(winSize/2)/fs), int(winSize/2+1))
Cep = xc[0 : len(quef)].real

plt.plot(quef, Cep)
plt.xlabel("Quefrency [ms]")
plt.ylabel("Cepstrum value")
plt.xlim([0,quef[-1]])
plt.ylim([-0.5, 0.5])

plt.show()
