#!/usr/bin/env python2
import argparse
import random
import os

random.seed()

parser = argparse.ArgumentParser(description="Generate random names via markov chain")
parser.add_argument("-n","--num",type=int, default=20, help="Number of names to generate")
parser.add_argument("-d","--degree",type=int, default=2, help="Degree of markov chain to use")
parser.add_argument("-f","--infile",default="",help="Input file of names to build chain")
parser.add_argument("-m","--maxlen",type=int,default=0,help="Override name max length")
parser.add_argument("-i","--minlen",type=int,default=0,help="Override name min length")
args = parser.parse_args()

f = open(args.infile,"r")
l = f.readlines()
f.close()

l = [s.rstrip().lstrip().lower() for s in l]
l = filter(lambda s: len(s) > 0 and not s.startswith('#'), l)

def addEntry(m, k1, k2):
  if k1 not in m.keys():
    m[k1] = {}
  if k2 not in m[k1].keys():
    m[k1][k2] = 1
  else:
    m[k1][k2] += 1

markov = {}
maxlen = 0
minlen = 100000000
for name in l:
  addEntry(markov,'',name[0])  
  for i in range(0,len(name)):
    addEntry(markov, name[max(0,i-args.degree):i], name[i])
  addEntry(markov, name[max(0,len(name)-args.degree):len(name)],'')
  if maxlen < len(name):
    maxlen = len(name)
  if minlen > len(name):
    minlen = len(name)

if args.maxlen > 0:
  maxlen = args.maxlen
if args.minlen > 0:
  minlen = args.minlen

for k1 in markov.keys():
  total = float(sum([markov[k1][k2] for k2 in markov[k1].keys()]))
  weights = []
  sumSoFar = 0.0
  # prefix sum, we meet again at last...
  for k2 in markov[k1].keys():
    weights.append((sumSoFar, k2))
    sumSoFar += markov[k1][k2] / total
  markov[k1] = weights


def chooseNextChar(m, prefix):
  weights = m[prefix]
  r = random.random()
  for i in range(0, len(weights)):
    (t, c) = weights[len(weights) - i - 1]
    if t <= r:
      return c

i=0
while i < args.num:
  # should use do-while, but syntax forgot...  does python even have?
  l = []
  l.append(chooseNextChar(markov, ''))
  while l[-1] != '':
    c = chooseNextChar(markov,''.join(l[max(0,len(l)-args.degree):len(l)]))
    l.append(c)
    #l.append(chooseNextChar(markov,''.join(l[max(0,len(l)-args.degree),len(l)])))
  l.pop()
  if len(l) <= maxlen and len(l) >= minlen:
    print ''.join(l).capitalize()
    i += 1

  
