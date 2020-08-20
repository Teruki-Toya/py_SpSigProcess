# -*- coding: utf-8 -*-

import numpy as np
import scipy.special

## ハニング窓
def winHann(winSize):

  n = np.linspace(0, 1, winSize)
  w = 0.5 - 0.5 * np.cos(2 * np.pi * n)
  
  return w

## サイン窓
def winSine(winSize):

  n = np.linspace(0, 1, winSize)
  w = np.sin(np.pi * n);
  
  return w
  
## カイザー窓
def winKaiser(alf, winSize):

  # sample index
  k = np.linspace(0, winSize-1, winSize)
  
  # beta coefficient (β = πα)
  bta = np.pi * alf;
  
  m = (k - winSize / 2) / (winSize / 2);
  numer = bta * np.sqrt(1 - m ** 2);
  
  w = scipy.special.jv(0, numer) / scipy.special.jv(0, bta)
  
  ### window :
  ### 	w = numer / denom
  ###
  ###	numer = J_0(bta * sqrt(1 - ((k - winSize/2) / (winSize/2) )^2 ))
  ###	denom = J_0(bta)
  ###	(J_0 : 0 次ベッセル関数)
  
  return w
