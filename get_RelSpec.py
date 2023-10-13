# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:30:45 2023

@author: Teruki Toya
"""

import soundfile as sf
import numpy as np
from scipy import interpolate
import analTemp
import analFreq
import matplotlib.pyplot as plt


# 音声データの取得
filepath = "snd/eng_per03.wav"
x_row, fs = sf.read(filepath)
x = x_row.T

x[0,:] = x[0,:] - np.mean(x[0,:])
x[1,:] = x[1,:] - np.mean(x[1,:])
x[2,:] = x[2,:] - np.mean(x[2,:])

# 時間をシンクロさせる
x[0,:] = analTemp.sigsTimeSyncronize(x[0,:], x[2,:])
x[1,:] = analTemp.sigsTimeSyncronize(x[1,:], x[2,:])

t_dul = (len(x[0,:])-1)/fs
t = np.linspace(0, t_dul, len(x[0,:]))

# 前後の無音区間をカット
t0 = 1.0    # 分析開始時刻 [s]
t1 = 10.9   # 分析終了時刻 [s]
xx = x[:, round(t0*fs):round(t1*fs)]

# スペクトル分析条件の指定
winSize = 256   # 分析窓長 [samples]
shiftSize = round(winSize / 2)  # フレームシフト長 [samples]
fftSize = winSize   # FFT長 [sample]

# フレームごとの短時間スペクトルを取得
X0_frm = analFreq.specByFrm(xx[0,:], fs, winSize, shiftSize, fftSize) # RT
X1_frm = analFreq.specByFrm(xx[1,:], fs, winSize, shiftSize, fftSize) # EC
X2_frm = analFreq.specByFrm(xx[2,:], fs, winSize, shiftSize, fftSize) # AC

# 長時間平均パワースペクトル（LTAS）の計算
X0p_mean = np.mean((X0_frm * X0_frm.conjugate()).real, axis=0)
X0p_mean = X0p_mean[0:round(fftSize/2)]
X1p_mean = np.mean((X1_frm * X1_frm.conjugate()).real, axis=0)
X1p_mean = X1p_mean[0:round(fftSize/2)]
X2p_mean = np.mean((X2_frm * X2_frm.conjugate()).real, axis=0)
X2p_mean = X2p_mean[0:round(fftSize/2)]

# 分析対象の周波数列
idx = np.linspace(0, round(fftSize/2)-1, round(fftSize/2))  # データインデックス
freq = idx * round(fs/2) / round(fftSize/2)   # 周波数列
k_5kHz = 30    # 5 kHz までの上限インデックス

## RT振動スペクトルの補正
#omg = 2*np.pi*freq  # 角周波数
#omg[0] = omg[1]
#X0p_meanC = X0p_mean / np.square(omg)

# 耳閉塞効果の補正データの生成
occEffData = np.loadtxt('data/occEffResp.csv', delimiter=',')
addFq = [20000, round(fs/2)]
addResp = [occEffData[1,occEffData.shape[1]-1], occEffData[1,occEffData.shape[1]-1]]
Fq = np.concatenate([[0], occEffData[0,:], addFq])
Resp = np.concatenate([[occEffData[1,0]], occEffData[1,:], addResp])
intpFunction = interpolate.PchipInterpolator(Fq, Resp)
intpResp = intpFunction(freq)

occEffPlot = plt.figure()
OEP = occEffPlot.add_subplot()
OEP.set_title("Occlusion Effect")
OEP.set_xlim([0, freq[-1]])
OEP.plot(freq, intpResp)

# EC音スペクトルの補正
X1p_meanC = X1p_mean / np.power(10, intpResp/10)

# 相対レベル[dB]表示
X0_dB = 10 * np.log10(X0p_mean/np.amax(X0p_mean))
X1_dB = 10 * np.log10(X1p_meanC/np.amax(X1p_meanC))
X2_dB = 10 * np.log10(X2p_mean/np.amax(X2p_mean))

X_all_dB = np.stack([freq, X0_dB, X1_dB, X2_dB], 0)
np.savetxt('data/eng_per03_LTAS_230706.csv', X_all_dB, delimiter=',')

# 骨導-気導相対スペクトルの計算
H0_dB = X0_dB - X2_dB           # 側頭部
H0_dB[0] = H0_dB[1]
#H0_dB[1] = H0_dB[2]

H1_dB = X1_dB - X2_dB           # 外耳道
H1_dB[0] = H1_dB[1]
#H1_dB[1] = H1_dB[2]

# 表現する周波数を 5 kHz までに制限
H0_dB_low = H0_dB[0:k_5kHz+1]  # 5 kHz までのデータを利用
H1_dB_low = H1_dB[0:k_5kHz+1]  # 5 kHz までのデータを利用

H0_dB_high = H0_dB_low[k_5kHz] * np.ones(len(H0_dB) - k_5kHz - 1) # 5 kHz以降はFlat
H1_dB_high = H1_dB_low[k_5kHz] * np.ones(len(H1_dB) - k_5kHz - 1) # 5 kHz以降はFlat

H0_dB_con = np.concatenate([H0_dB_low, H0_dB_high])
H1_dB_con = np.concatenate([H1_dB_low, H1_dB_high])

H0_dB_con = H0_dB_con - np.amax(H0_dB_con)
H1_dB_con = H1_dB_con - np.amax(H1_dB_con)

H_all_dB = np.stack([freq, H0_dB_con, H1_dB_con], 0)
np.savetxt('data/eng_per03_relSpec_230706.csv', H_all_dB, delimiter=',')

# 波形のプロット
c0,c1,c2 = "blue","red","black"     # 各プロットの色

wavForm = plt.figure()
wf0 = wavForm.add_subplot(311)
wf0.set_title("Ch. 0 - Regio-temporalis BC", color=c0)
wf0.set_xlim([0, t[-1]])
wf0.set_xticklabels(["", "", "", "", "", "", "", ""])
wf0.set_ylim([-1, 1])
wf0.plot(t, x[0, :], color=c0)

wf1 = wavForm.add_subplot(312)
wf1.set_title("Ch. 1 - Ear-canal BC", color=c1)
wf1.set_ylabel("Amplitude")
wf1.set_xlim([0, t[-1]])
wf1.set_xticklabels(["", "", "", "", "", "", "", ""])
wf1.set_ylim([-1, 1])
wf1.plot(t, x[1, :], color=c1)

wf2 = wavForm.add_subplot(313)
wf2.set_title("Ch. 2 - AC", color=c2)
wf2.set_xlabel("Time [s]")
wf2.set_xlim([0, t[-1]])
wf2.set_ylim([-1, 1])
wf2.plot(t, x[2, :], color=c2)

# LTAS のプロット
LTAS = plt.figure()
ls0 = LTAS.add_subplot(311)
ls0.set_title("Ch. 0 - Mastoid BC", color=c0)
ls0.set_xlim([0, 5000])
ls0.set_xticklabels(["", "", "", "", "", "", "", "", ""])
ls0.set_ylim([-60, 5])
ls0.plot(freq, X0_dB, color=c0)

ls1 = LTAS.add_subplot(312)
ls1.set_title("Ch. 1 - Ear-canal BC", color=c1)
ls1.set_ylabel("Relative Level [dB]")
ls1.set_xlim([0, 5000])
ls1.set_xticklabels(["", "", "", "", "", "", "", "", ""])
ls1.set_ylim([-60, 5])
ls1.plot(freq, X1_dB, color=c1)

ls2 = LTAS.add_subplot(313)
ls2.set_title("Ch. 2 - AC", color=c2)
ls2.set_xlabel("Frequency [Hz]")
ls2.set_xlim([0, 5000])
ls2.set_ylim([-60, 5])
ls2.plot(freq, X2_dB, color=c2)

# 相対スペクトルのプロット
relSpec = plt.figure()
rs0 = relSpec.add_subplot(211)
rs0.set_title("|H_ob|", color=c0)
rs0.set_ylabel("Relative Level [dB]")
rs0.set_xlim([0, 20000])
rs0.set_xticklabels(["", "", "", "", "", "", "", "", ""])
rs0.set_ylim([-40, 5])
rs0.plot(freq, H0_dB_con, color=c0)

rs1 = relSpec.add_subplot(212)
rs1.set_title("|H_oc|", color=c1)
rs1.set_xlabel("Frequency [Hz]")
rs1.set_xlim([0, 20000])
rs1.set_ylim([-40, 5])
rs1.plot(freq, H1_dB_con, color=c1)

plt.show()