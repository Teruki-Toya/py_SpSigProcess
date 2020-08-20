# -*- coding: utf-8 -*-

import numpy as np
import scipy.fftpack as spfft
import wdFunc
import lpcas

## 周波数スペクトル
def spectrum(x, fs, fftSize):
  if fftSize % 2 == 1:
    fftSize = fftSize + 1

  # 分析窓をかける
  w = wdFunc.winHann(len(x))
  xw = x * w
  
  # 高速フーリエ変換（FFT）
  X = spfft.fft(xw, fftSize)
  
  # 分析対象の周波数列
  idx = np.linspace(0, int(fftSize/2), int(fftSize/2+1))
  freq = idx * fs / fftSize
  
  # 振幅スペクトル
  S_amp = 20 * np.log10(abs(X))
  S_amp = S_amp[0 : len(freq)]
  
  # 位相スペクトル
  S_phase = np.angle(X)
  S_phase = S_phase[0 : len(freq)]
  
  return freq, S_amp, S_phase


## スペクトログラム
def spgram(x, fs, winSize, *, shiftC = 4, fftC = 5):
  if winSize % 2 == 1:
    winSize = winSize + 1
  
  # 窓のシフト長
  shiftSize = round(winSize / shiftC)
  if shiftSize % 2 == 1:
    shiftSize = shiftSize + 1
  
  # FFT長
  fftSize = winSize * fftC
  
  # 総フレーム数
  N_frame = np.floor((len(x) - (winSize - shiftSize)) / shiftSize)
  N_frame_int = N_frame.astype(np.int)
  
  # 周波数 - 時間のスペクトル行列
  Sa = np.zeros((N_frame_int, round(fftSize / 2) + 1))
  for frame in range(N_frame_int):
    offset = shiftSize * frame		# フレームをシフトしながら
    s = x[offset : offset + winSize]
    freq, Sa_tmp, Sp = spectrum(s, fs, fftSize) # スペクトル分析
    Sa[frame, :] = Sa_tmp[::-1]
  
  SaT = Sa.T 		# 転置（時間を横方向、周波数を縦方向に）
  ids = np.linspace(0, N_frame_int - 1, N_frame_int)
  t = ids * shiftSize / fs  # 時間サンプル列
  
  return t, freq, SaT


## ケプストラム
def cepstrum(x, fftSize):
  
  # 分析窓をかける
  w = wdFunc.winHann(len(x))
  xw = x * w
  
  # 高速フーリエ変換（FFT）
  X = spfft.fft(xw, fftSize)
  
  # 対数スペクトル
  A = np.log10(abs(X))
  
  # 逆フーリエ変換
  xc = spfft.ifft(A, fftSize)

  return xc


## ケプストラム法によるスペクトル包絡の分析
def spcrmEnv_cepst(x, fs, liftSize, *, fftC = 1):
  
  # FFT長
  fftSize = len(x) * fftC
  
  # ケプストラム
  xc = cepstrum(x, fftSize)
  
  # 低ケフレンシ成分以外を 0 埋め
  xc[liftSize : len(xc) - liftSize] = np.zeros(len(xc) - 2 * liftSize)

  # 低ケフレンシ成分のフーリエ変換
  XC = spfft.fft(xc, fftSize)
  
  # 分析対象の周波数列
  idx = np.linspace(0, int(fftSize/2), int(fftSize/2+1))
  freq = idx * fs / fftSize
  
  # dB 表現（すでに対数スペクトルになっているので、20 のみ乗算）
  XC_amp = 20 * XC.real
  XC_amp = XC_amp[0 : len(freq)]
  
  return freq, XC_amp


## 線形予測（LP）によるスペクトル包絡の分析
def spcrmEnv_lpc(x, fs, lpcOrder, *, fftC = 5, preEnp = 1, coeff = 0.98):
  
  # FFT長
  fftSize = len(x) * fftC
  
  # プリエンファシス
  if preEnp == 0:
    x0 = x
  else:
    xtmp = np.append(0, x[0 : len(x) - 1])
    x0 = x - coeff * xtmp
    x0[0] = 0
  
  # 分析窓をかける
  w = wdFunc.winHann(len(x))
  x0w = x0 * w
  
  # 線形予測分析
  x_lpc, parcor = lpcas.LDcalc(x0w, lpcOrder)
  
  # フーリエ変換
  X = spfft.fft(x_lpc, fftSize)
  
  # 分析対象の周波数列
  idx = np.linspace(0, int(fftSize/2), int(fftSize/2+1))
  freq = idx * fs / fftSize
  
  # 声道順フィルタ（分子／分母が逆転（dB 表現では符号反転））
  VTfilt = -20 * np.log10(abs(X))
  VTfilt = VTfilt[0 : len(freq)]
  
  return freq, VTfilt
