#!/usr/bin/python2

import random
import argparse
import math

random.seed()

def roll(instr):
  if ',' in instr:
    [instr,prob] = instr.split(',')
    prob = float(prob)
  else: prob = 1.0
  if 'x' in instr:
    [instr,mult] = instr.split('x')
    mult = int(mult)
  else: mult = 1
  if '-' in instr:
    [instr,sub] = instr.split('-')
    sub = int(sub)
  else: sub = 0
  if 'd' in instr:
    [n,m] = instr.split('d')
    n = int(n)
    m = int(m)
  else:
    n = int(instr)
    m = 1
  total = 0
  if random.random() < prob:
    for i in xrange(n):
      total += random.randint(1,m)
    total -= sub
    total *= mult
  return total

def doLine(marketclass, line, numMonths):
  if len(line) < 6:
    print line[0]
  else:
    total = 0
    for i in xrange(numMonths):
      total += roll(line[marketclass])
    if total > 0:
      week1 = int(math.ceil(total/2.0))
      week2 = int(math.ceil((total-week1)/2.0))
      week3 = total - week1 - week2
      print line[0] + ': ' + str(total) +" ("+str(week1)+"/"+str(week2)+"/"+str(week3)+")"


parser = argparse.ArgumentParser(description="Generate mercs avail in town")
parser.add_argument("-m","--market",type=int, default=4,help="Market class to gen for")
parser.add_argument("-f","--inFile",default="./hireprices",help="File of merc avails by market")
parser.add_argument("-n","--numMonths",type=int,default=1,help="Number of months to gen for")
args = parser.parse_args()

infile = open(args.inFile,"r")
lines = infile.readlines()
infile.close()
lines = filter(lambda s: not s.startswith('#'), lines)
lines = map(lambda k: k.lstrip().rstrip(), lines)
lines = map(lambda k: k.split(":"), lines)

for line in lines:
  doLine(args.market, line, args.numMonths)
