# -*- coding: utf-8 -*-

import sounddevice as sd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from scipy import signal

sd.default.device = [27, 26] # Input, Output�f�o�C�X�w��

def callback(indata, frames, time, status):
    # indata.shape=(n_samples, n_channels)
    global plotdata
    data = indata[::downsample, 0]
    shift = len(data)
    plotdata = np.roll(plotdata, -shift, axis=0)
    plotdata[-shift:] = data


def update_plot(frame):
    """This is called by matplotlib for each plot update.
    """
    global plotdata, window
    x = plotdata[-N:] * window
    F = np.fft.fft(x) # �t�[���G�ϊ�
    F = F / (N / 2) # �t�[���G�ϊ��̌��ʂ𐳋K��
    F = F * (N / sum(window)) # ���֐��ɂ��␳
    Amp = np.abs(F) # �U���X�y�N�g��
    line.set_ydata(Amp[:N // 2])
    return line,

downsample = 1  # FFT����̂Ń_�E���T���v�����O�͂��Ȃ�
length = int(1000 * 44100 / (1000 * downsample))
plotdata = np.zeros((length))
N =2048            # FFT�p�̃T���v����
fs = 44100            # �����f�[�^�̃T���v�����O���g��
window = signal.hann(N) # ���֐�
freq = np.fft.fftfreq(N, d=1 / fs) # ���g���X�P�[��

fig, ax = plt.subplots()
line, = ax.plot(freq[:N // 2], np.zeros(N // 2))
ax.set_ylim([0, 1])
ax.set_xlim([0, 3000])
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Amplitude spectrum')
fig.tight_layout()

stream = sd.InputStream(
        channels=1,
        dtype='float32',
        callback=callback
    )
ani = FuncAnimation(fig, update_plot, interval=30, blit=True)
with stream:
    plt.show()
