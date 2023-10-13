# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:30:45 2023

@author: Teruki Toya
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt


filepath = "snd/eng_per03.wav"

x, fs = sf.read(filepath)

t_dul = (len(x)-1)/fs
t = np.linspace(0, t_dul, len(x))

# プロット
c1,c2,c3 = "blue","green","red"     # 各プロットの色

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.set_title("Ch. 0 - Mastoid BC", color=c1)
ax1.set_xlim([0, t[-1]])
ax1.set_xticklabels(["", "", "", "", "", "", "", ""])
ax1.set_ylim([-1, 1])
ax1.plot(t, x[:, 0], color=c1)

ax2 = fig.add_subplot(312)
ax2.set_title("Ch. 1 - Ear-canal BC", color=c2)
ax2.set_ylabel("Amplitude")
ax2.set_xlim([0, t[-1]])
ax2.set_xticklabels(["", "", "", "", "", "", "", ""])
ax2.set_ylim([-1, 1])
ax2.plot(t, x[:, 1], color=c2)

ax3 = fig.add_subplot(313)
ax3.set_title("Ch. 2 - AC", color=c3)
ax3.set_xlabel("Time [s]")
ax3.set_xlim([0, t[-1]])
ax3.set_ylim([-1, 1])
ax3.plot(t, x[:, 2], color=c3)

plt.show()