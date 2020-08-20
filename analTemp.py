# -*- coding: utf-8 -*-

import numpy as np

def corrAuto(x, *, order = 0):
  if order <= 0:
    r = np.zeros(len(x))
  else:
    r = np.zeros(order + 1)

  for m in range(len(r)):
    for n in range(len(x) - m):
      r[m] = r[m] + x[n] * x[n + m]
  
  return r
