# -*- coding: utf-8 -*-

import wave
from scipy import fromstring, int16

## WAV ファイルを数値配列に変換
def wav2int(wavFile):
  
  # WAV ファイルを開く
  wr = wave.open(wavFile, "rb")

  # WAVファイルの情報を表示したいとき
  '''
  print "Channel num : ", wr.getnchannels()
  print "Sample size : ", wr.getsampwidth()
  print "Sampling rate : ", wr.getframerate()
  print "Frame num : ", wr.getnframes()
  print "Prams : ", wr.getparams()
  print "Sec : ", float(wr.getnframes()) / wr.getframerate()
  '''
  
  Rd  = (2**8) ** wr.getsampwidth() / 2
  fs = wr.getframerate()

  # データの読み込み
  data = wr.readframes(wr.getnframes())

  # 文字型から数値型に
  x = fromstring(data, dtype = int16)
  x = x / Rd

  wr.close()
  
  return x, fs
