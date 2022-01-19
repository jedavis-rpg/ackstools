#!/usr/bin/python
import random

random.seed()

# zero-level caster gets no spells, and cheap indexing

spellsbylevel=[\
  [0, 0, 0, 0, 0, 0],\
  [1, 0, 0, 0, 0, 0],\
  [2, 0, 0, 0, 0, 0],\
  [2, 1, 0, 0, 0, 0],\
  [2, 2, 0, 0, 0, 0],\
  [2, 2, 1, 0, 0, 0],\
  [2, 2, 2, 0, 0, 0],\
  [3, 2, 2, 1, 0, 0],\
  [3, 3, 2, 2, 0, 0],\
  [3, 3, 3, 2, 1, 0],\
  [3, 3, 3, 3, 2, 0],\
  [4, 3, 3, 3, 2, 1],\
  [4, 4, 3, 3, 3, 2],\
  [4, 4, 4, 3, 3, 2],\
  [4, 4, 4, 4, 3, 3] ]


def selRandFromList(num, seq):
  if num <= 0:
    return []
  if (num >= len(seq)):
    return seq
  alreadygot = []
  # this implementation is awful for speed.  Whooo python
  for i in range(0,num):
    ind = random.randint(0,len(seq)-1)
    while ind in alreadygot:
      ind = random.randint(0,len(seq)-1)
    alreadygot.append(ind)
  return map(lambda l: seq[l], alreadygot)

def parseSpells(infile):
  sfdesc = open(infile, 'r')
  spelllist = sfdesc.readlines()
  sfdesc.close()
  spelllist = filter(lambda s: not s.startswith('#'), spelllist)
  spelllist = map(lambda k: k.lstrip().rstrip(), spelllist)
  outlist = []
  while spelllist != []:
    tmp = []
    spellname = spelllist.pop(0)
    while spellname != "" and spelllist != []:
      tmp.append(spellname)
      if spelllist != []:
        spellname = spelllist.pop(0)
    outlist.append(tmp)
  return outlist

def genSpells(slist, level, intel, excess):
  out = []
  for i in range(0,len(slist)):
    numspells = spellsbylevel[level][i]
    if numspells > 0:
      numspells += intel
      if excess:
        numspells += random.randint(0,2) 
    tmp = selRandFromList(numspells,slist[i])
    if tmp != []:
      out.append(tmp)
  return out

def printSpells(known):
  for j in range(0,len(known)):
    print "" + str(j+1) + ": " + ', '.join(known[j])
