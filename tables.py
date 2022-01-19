#!/usr/bin/python

# library for loading and rolling on random tables

import re
import random

dicereg = re.compile('(\d+)d(\d+)')
tabledicereg = re.compile('^(\d+)d(\d+)$')
# I could probably do arbitrary-length sums with (\d*)(\+\d*)+...
# except that if I do this, python will only store the value of the last +group
# so this is good enough for now
plusreg = re.compile('(\d+)\+(\d+)')
multreg = re.compile('(\d+)x(\d+)')
multitablereg = re.compile('\[([a-zA-Z0-9]+)\*(\d+)\]')
tablereg = re.compile('\[([a-zA-Z0-9]+)\]')
probreg = re.compile('\((.+?)\)%(0\.\d+)')

random.seed()

def subsum(match):
  if len(match.groups()) != 2:
    return "Error"
  return str(int(match.group(1)) + int(match.group(2)))

def submult(match):
  if len(match.groups()) != 2:
    return "Error"
  return str(int(match.group(1)) * int(match.group(2)))

def simpleroll(a,b):
  c=0
  for i in range(0,int(a)):
    c+=random.randint(1,int(b))
  return c

def subdice(match):
  if len(match.groups()) != 2:
    return "Error"
  return str(simpleroll(int(match.group(1)),int(match.group(2))))

def submultitable(match):
  if len(match.groups()) != 2:
    return "Error"
  acc = []
  for i in range(0, int(match.group(2))):
    acc.append('[' + match.group(1) + ']')
  return ', '.join(acc)

def subtable(match):
  if len(match.groups()) != 1:
    return "Error"
  return evaltable(match.group(1))

def subprob(match):
  if len(match.groups()) != 2:
    return "Error"
  p = float(match.group(2))
  r = random.random()
  if r < p:
    return match.group(1)
  else:
    return ""

# map of table names to dice to roll on them
tabledice = {}
# map of table names to lists of (number, entry) pairs
tableentries = {}

def process(entry):
  entry = probreg.sub(subprob, entry)
  entry = dicereg.sub(subdice, entry)
  entry = dicereg.sub(subdice, entry)
  entry = multreg.sub(submult, entry)
  entry = plusreg.sub(subsum, entry)
  entry = multitablereg.sub(submultitable, entry)
  entry = tablereg.sub(subtable, entry)
  return entry

def evaltable(tablename):
  (numtoroll, diesize) = tabledice[tablename]
  ind = simpleroll(numtoroll, diesize)
  l = tableentries[tablename]
  cands = filter(lambda (i, s): i >= ind, l)
  if cands == []:
    print "ERROR: " + tablename + " and index "+ str(ind) +" explodes."
    print l
  entry = cands[0][1]
  # if cands has length 0, we have other problems
  return process(entry).rstrip(', ').lstrip(', ')

def loadtables(fname):
  f = open(fname, 'r')
  lines = f.readlines()
  f.close()
  comments = [s[1:].rstrip().lstrip() for s in filter(lambda l: l.startswith('#'),lines)]
  # get our #includes, basically
  worklist = [s[5:] for s in comments if s.startswith('LOAD ')]
  lines = filter(lambda l: not l.startswith('#'), lines)
  lines = map(lambda l: l.lstrip().rstrip(), lines)
  while lines != []:
    tname = lines.pop(0)
    dice = lines.pop(0)
    tableentries[tname] = []
    dm = tabledicereg.match(dice)
    # if no dice definition, we do one of two things:
    # if no numbering on entries, we assume all equal weight
    # if numbering on entries, we assume a dN where n is number
    # of last entry
    # if we do have a dice definition, we use that instead
    if dm:
      tabledice[tname] = dm.groups()
      e = lines.pop(0)
    else:
      e = dice
    count = 0
    while e != "":
      while e.endswith('/'):
        e = e.rstrip("/")
        e += lines.pop(0)
      splot = e.split(': ',1)
      if len(splot) > 1:
        count = int(splot[0])
        e = splot[1]
      else:
        count += 1
      tableentries[tname].append((count, e))
      if lines != []:
        e = lines.pop(0)
      else:
        e = ""
    if tname not in tabledice:
      tabledice[tname] = ("1",str(count))
  for f in worklist:
    loadtables(f)
