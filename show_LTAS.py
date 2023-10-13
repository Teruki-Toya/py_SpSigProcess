# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import analFreq

wavFile = "snd/vowelTest.wav"
x, fs = sf.read(wavFile, always_2d=True)
t_dul = (len(x)-1)/fs
t = np.linspace(0, t_dul, len(x))

# # 分析する音の開始・終了区間[s]
# t_start = 0.5
# t_end = 3.5

# 分析窓長 [samples]
winSize = 256
  
# フレームシフト長 [samples]
shiftSize = round(winSize / 2)

# FFT長 [sample]
fftSize = winSize * 4

# p_start = round(fs * t_start)
# p_end = round(fs * t_end)

# xw = x[p_start : p_end]
xw1 = x[:, 0]
xw2 = x[:, 1];

X1_frm = analFreq.specByFrm(xw1, fs, winSize, shiftSize, fftSize)
X2_frm = analFreq.specByFrm(xw2, fs, winSize, shiftSize, fftSize)

X1_mean = np.mean(X1_frm, axis=0)
X2_mean = np.mean(X2_frm, axis=0)

# 分析対象の周波数列
idx = np.linspace(0, int(fftSize/2), int(fftSize/2+1))
freq = idx * fs / fftSize

# 振幅スペクトル
S1_amp = 20 * np.log10(abs(X1_mean))
S1_amp = S1_amp[0 : len(freq)]
S1_amp = S1_amp - np.amax(S1_amp)

S2_amp = 20 * np.log10(abs(X2_mean))
S2_amp = S2_amp[0 : len(freq)]
S2_amp = S2_amp - np.amax(S2_amp)

S_diff = S2_amp - S1_amp
S_diff = S_diff - np.amax(S_diff)

# # プロット
# plt.plot(freq, S_amp)
# plt.title("Amplitude Spectrum")
# plt.xlabel("Frequency [Hz]", fontsize = 13)
# plt.ylabel("Magnitude [dB]", fontsize = 13)
# plt.xlim([0,freq[-1]])
# plt.tick_params(labelsize=10)

fig1 = plt.figure()
ax1 = fig1.add_subplot(211)
ax1.set_title("Ch. 1", color="blue")
ax1.set_ylabel("Relative Level [dB]")
ax1.set_xlim([0,5000])
ax1.plot(freq,S1_amp)

ax2 = fig1.add_subplot(212)
ax2.set_title("Ch. 2", color="blue")
ax2.set_xlabel("Frequency [Hz]")
ax2.set_ylabel("Relative Level [dB]")
ax2.set_xlim([0,5000])
ax2.plot(freq,S2_amp)

fig1.savefig("fig/LTAS_4.png", bbox_inches='tight')

# plt.show()

fig2 = plt.figure()
ax3 = fig2.add_subplot(111)
ax3.set_title("BC re AC spectrum", color="blue")
ax3.set_xlabel("Frequency [Hz]")
ax3.set_ylabel("Relative Level [dB]")
ax3.set_xlim([0,5000])
ax3.plot(freq,S_diff)

fig2.savefig("fig/S_diff_4.png", bbox_inches='tight')

plt.show()
