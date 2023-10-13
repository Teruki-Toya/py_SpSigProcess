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

def sigsTimeSyncronize(sig1, sig0):
  if len(sig0) > len(sig1):
    sig1 = sig1, np.zeros(len(sig0)-len(sig1))
  elif len(sig0) < len(sig1):
    sig1 = sig1[0:len(sig0)]
  
  c = np.correlate(sig1, sig0, "full")
  d = c.argmax() - (len(sig0) - 1)
  
  if d > 0:
    sig1r = np.concatenate([sig1[d:], sig1[0:d]])
  elif d < 0:
    sig1r = np.concatenate([sig1[len(sig1)+d:], sig1[0:len(sig1)+d]])

  return sig1r