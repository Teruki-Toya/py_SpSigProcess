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
t_anal = 1.1

# 分析窓長 [s]
winSec = 200 * (10 ** -3)

p_anal = round(fs * t_anal)
winSize = round(fs * winSec)

if winSize % 2 == 1:
  winSize = winSize + 1

i_ini = round(p_anal - winSize / 2)
i_fin = round(p_anal + winSize / 2)
xw = x[i_ini : i_fin]

[freq, S_amp, S_phase] = analFreq.spectrum(xw, fs, winSize)

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.set_title("Amplitude Spectrum", color="blue")
ax1.set_ylabel("Amplitude [dB]")
ax1.set_xlim([0,freq[-1]])
ax1.plot(freq,S_amp)

ax2 = fig.add_subplot(212)
ax2.set_title("Phase Spectrum", color="blue")
ax2.set_xlabel("Frequency [Hz]")
ax2.set_ylabel("Phase [rad]")
ax2.set_xlim([0,freq[-1]])
ax2.plot(freq,S_phase)

plt.show()
