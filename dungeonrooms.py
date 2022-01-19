#!/usr/bin/python2

import random
import sys


random.seed()
num = int(sys.argv[1])
out = []
for i in range(0,num):
  roll = random.randint(1,20)
  if roll <= 6:
    if random.random() < 0.15:
      out.append("Empty with treasure")
    else:
      out.append("Empty")
  elif roll <= 12:
    out.append("Monster")
  elif roll <= 15:
    if random.random() < 0.3:
      out.append("Trap with treasure")
    else:
      out.append("Trap")
  else:
    out.append("Unique")
out.sort()
print '\n'.join(out)
