# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import wavRead
import analFreq

wavFile = "＜分析したいオーディオデータ（のパス）＞.wav"
x, fs = wavRead.wav2int(wavFile)
t_dul = (len(x)-1)/fs
t = np.linspace(0, t_dul, len(x))

# 分析窓長 [s]
winSec = 100 * (10 ** -3)

winSize = round(fs * winSec)

if winSize % 2 == 1:
  winSize = winSize + 1

t, freq, Sa = analFreq.spgram(x, fs, winSize)

plt.imshow(Sa, cmap="jet", extent=[0, t[-1], 0, freq[-1]], aspect="auto")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.colorbar()
plt.show()
