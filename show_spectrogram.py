# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import analFreq

# 音声データの取得
filepath = "snd/text.wav"
x_row, fs = sf.read(filepath)
x = x_row[18405:190000].T

#x = x[0,:];
t_dul = (len(x)-1)/fs
t = np.linspace(0, t_dul, len(x))


# 分析窓長
winSize = 256;
shiftSize = round(winSize/2)

t, freq, Sa = analFreq.spgram(x, fs, winSize, shiftSize)

plt.imshow(Sa, cmap="jet", extent=[0, t[-1], 0, freq[-1]], aspect="auto", vmin=-100, vmax=10)
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
#plt.xlim([1, 2])
plt.ylim([0, 22050])
plt.colorbar()
plt.show()
