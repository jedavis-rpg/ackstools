#!/usr/bin/python
import random

random.seed()

def die(n):
  return random.randint(1,n)

def dice(n,m):
  a = 0
  for b in range(n):
    a += random.randint(1,m)
  return a

def roll(t):
  if len(t) == 1:
    return die(t[0])
  elif len(t) == 2:
    return dice(t[0],t[1])
  elif len(t) > 2:
    return dice(t[0],t[1]) + t[2]
  else:
    return -1 # consider doing better error condition design

def parse(s):
  # takes strings of the form n, ndm, or ndm+k and converts to tuple for 
  # roll
  addl = s.split('+')
  dl = addl[0].split('d')
  if len(addl) > 1 and len(dl) > 1:
    return (int(dl[0]), int(dl[1]), int(addl[1]))
  elif len(dl) > 1:
    return (int(dl[0]), int(dl[1]))
  else:
  # given n, return a tuple which yields a constant when rolled
    return (1, 1, int(dl[0])-1)
  
