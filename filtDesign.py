# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 15:13:36 2023

@author: Teruki Toya
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

fs = 44100     # サンプリング周波数 [Hz]

# 相対スペクトルのデータを読み込む
H_all_dB = np.loadtxt('data/eng_per03_relSpec_230706.csv', delimiter=',')
freq = H_all_dB[0,:]
freq[-1] = round(fs/2)  # 終端をナイキスト周波数に調整

H0_dB = H_all_dB[1,:]  # 側頭部振動
H1_dB = H_all_dB[2,:]  # 外耳道内放射

# フィルタ設計
Ntap = 513;    # FIR タップ数
firH0 = signal.firls(Ntap, freq, np.power(10, H0_dB/20), fs=fs)
firH1 = signal.firls(Ntap, freq, np.power(10, H1_dB/20), fs=fs)

# フィルタの周波数応答を確認
w0, h0 = signal.freqz(firH0)
w1, h1 = signal.freqz(firH1)

# プロット
c0,c1,c2 = "blue","red","black"     # 各プロットの色

filtChar = plt.figure()
fcr0 = filtChar.add_subplot(211)
fcr0.plot(w0*fs/(2*np.pi), 20*np.log10(abs(h0)), color=c0)
fcr0.plot(freq, H0_dB, ':', color=c2)
fcr0.set_title("|H_ob| filter", color=c0)
fcr0.set_ylabel("Gain [dB]")
fcr0.set_xticklabels(["", "", "", "", "", "", "", "", ""])
fcr0.set_ylim([-50, 5])
fcr0_phs = fcr0.twinx()
phi0 = np.unwrap(np.angle(h0))
fcr0_phs.plot(w0*fs/(2*np.pi), phi0, "-.", color='g')
fcr0_phs.set_ylabel('Phase [rad]', color='g')
fcr0_phs.axis('tight')
fcr0.set_xlim([0, 5000])
fcr0_phs.set_ylim([-200, 5])

fcr1 = filtChar.add_subplot(212)
fcr1.plot(w1*fs/(2*np.pi), 20*np.log10(abs(h1)), color=c1)
fcr1.plot(freq, H1_dB, ':', color=c2)
fcr1.set_title("|H_oc| filter", color=c1)
fcr1.set_xlabel("Frequency [Hz]")
fcr1.set_ylim([-50, 5])
fcr1_phs = fcr1.twinx()
phi1 = np.unwrap(np.angle(h1))
fcr1_phs.plot(w1*fs/(2*np.pi), phi1, "-.", color='g')
fcr1_phs.axis('tight')
fcr1.set_xlim([0, 5000])
fcr1_phs.set_ylim([-200, 5])

plt.show()