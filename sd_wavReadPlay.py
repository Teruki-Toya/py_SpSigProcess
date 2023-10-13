# -*- coding: utf-8 -*-

import numpy as np
import soundfile as sf
import sounddevice as sd

sd.default.device = [1, 8] # Input, Outputデバイスを指定

# WAVファイルの相対パス
wavFilePath = "snd/eng_per03.wav"

# WAV ファイルを読み込み変数に格納
x, fs = sf.read(wavFilePath)
sd.play(x[:, 1], fs)
