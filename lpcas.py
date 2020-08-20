# -*- coding: utf-8 -*-

import numpy as np
import analTemp

## Levinson-Durbin 法によるLPC計算
def LDcalc(x, lpcOrder):

  # パラメータ（初期値 0 埋め）
  a = np.zeros(lpcOrder + 1)
  lpc = np.zeros(lpcOrder + 1)
  gamma = np.zeros(lpcOrder + 1)
  epsilon = np.zeros(lpcOrder + 1)
  
  # 自己相関
  r = analTemp.corrAuto(x, order = lpcOrder)
  
  # パラメータ ε, γ, lpc の設定
  epsilon[0] = r[0]
  gamma[1] = -r[1] / epsilon[0]
  lpc[0] = 1
  lpc[1] = gamma[1]
  epsilon[1] = epsilon[0] * (1 - (gamma[1] ** 2))
  
  # lpc と parcor 係数の計算
  ix = np.linspace(0, lpcOrder, lpcOrder + 1)
  ix = ix.astype(np.int)
  for m in ix[2 : len(ix)]:
    for n in range(m):
      a[n] = lpc[n]
	
    a[m] = 0
    num = 0
	
    for n in range(m + 1):
      num = num + a[n] * r[m - n]
	
    gamma[m] = -num / epsilon[m - 1]
	
    for n in range(m + 1):
      lpc[n] = a[n] + gamma[m] * a[m - n]
	
    epsilon[m] = epsilon[m - 1] * (1 - (gamma[m] ** 2))
  
  parcor = -gamma
  
  return lpc, parcor
