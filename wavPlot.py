# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import wavRead

# WAV ファイルのパス
wavFile = "＜オーディオデータ（のパス）＞.wav"

# WAV ファイルを数値配列に変換
x, fs = wavRead.wav2int(wavFile)

t_dul = (len(x)-1)/fs
t = np.linspace(0, t_dul, len(x))

# プロット
plt.plot(t, x)
plt.xlabel("Time [s]", fontsize = 13)
plt.ylabel("Amplitude", fontsize = 13)
plt.xlim([0,t_dul])
plt.ylim([-1,1])
plt.tick_params(labelsize=10)

plt.show()
