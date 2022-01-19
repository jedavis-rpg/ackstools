#!/usr/bin/python2
import random
import math
import libspellbook
import tables
import re

random.seed()

qualweights = []

marketClasses = [\
  [[4,100],[5,10],[3,10],[1,10],[1,6]],\
  [[5,20],[2,6],[2,4],[1,3],[1,2]],\
  [[4,8],[1,4],[1,3],[.85],[.45]],\
  [[3,4],[1,2],[1],[.33],[.15]],\
  [[1,6],[.65],[.4],[.15],[.05]],\
  [[1,2],[.2],[.15],[.05],[0]]]

alignments = ["C","N","N","N","L","L"]

# TODO make this loadable in parseClasses / add to classfile format
casters = { "mage":1, "elven spellsword":1,"elven nightblade":0.5,\
  "elven courtier":0.5, "elven enchanter":1, "gnomish trickster":0.5,\
  "nobiran wonderworker":1,"warlock":0.67, "elven warlock":1.0}
  
itemtable = {'W': "Sword", 'S': "Scroll", 'A': "Armor", 'M': "MiscWeapon",
'R': "Wand", 'P':"Potion",'I':"Ring",'C':"MiscMagic"}

# stuff everyone can use
itemsprefix = "PIC"

def mod(n):
  if n >= 18:
    return 3
  elif n >= 16:
    return 2
  elif n >= 13:
    return 1
  elif n >= 9:
    return 0
  elif n >= 6:
    return -1
  elif n >= 3:
    return -2
  else:
      return -3

def rollMarket(l):
  if len(l) > 1:
    acc = 0
    for i in range(0,l[0]):
      acc += random.randint(1,l[1])
    return acc
  elif l[0] > 0 and l[0] < 1:
    if random.randint(1,100) <= l[0] * 100:
      return 1
    else: 
      return 0
  else:
    return l[0]

# weight values for prime reqs
def primeReq(a, arr):
  if arr[a-1] >= 16:
    return qualweights[1]
  elif arr[a-1] >= 13:
    return qualweights[2]
  elif arr[a-1] >= 9:
    return qualweights[3]
  else:
    return 0

def minsWeight(a,b,arr):
  if arr[a-1] >= b:
    return qualweights[0]
  else:
    return 0
  
def parseClasses(classfilename):
  # open and read in file
  # TODO error handling
  cfdesc = open(classfilename,'r')
  classlist = cfdesc.readlines()
  cfdesc.close()
  # strip comments
  classlist = filter(lambda s: not s.startswith('#'), classlist)
  # load the quals weight array
  # current implementation is based on number of classes
  # TODO make configurable directly in class files
  for i in range(0,4):
    qualweights.append(len(classlist) ** (3-i))
  outlist = []
  # structure of output list is list of tuples containing
  # name of class
  # class HD
  # list of weight functions for class
  # list of permitted magic items
  # gender ratio
  # general frequency multiplier
  # This is terrible and despite my loathing for them 
  # I should use an object here
  for s in classlist:
    tmp = s.split(", ")
    # get class name
    name = tmp.pop(0)
    hd = tmp.pop(0)
    # relative frequency of this class
    freq = float(tmp.pop(0))
    items = tmp.pop(0)
    gender = tmp.pop(0)
    reqs = []
    for score in tmp:
      score.rstrip().lstrip()
      minslist = score.split(' ')
      minslist = map(int, minslist)
      if len(minslist) == 1:
        # mmm...  curry
        reqfn = (lambda x: (lambda arr: primeReq(x, arr)))(int(score))
      else:
        minstat = (minslist[0], minslist[1])
        reqfn = (lambda x,y: (lambda arr: minsWeight(x,y,arr))) (minstat[0], minstat[1])
      reqs.append(reqfn)
    outlist.append((name, hd, reqs, list(itemsprefix + items), gender, freq))
  return outlist

def parseNames(namefile):
  nf = open(namefile,"r")
  names = nf.readlines()
  nf.close()
  names = [c.rstrip().lstrip() for c in names]
  names = filter(lambda s: not s.startswith('#'), names)
  out = {}
  i = names.index("")
  out['M'] = names[0:i]
  out['F'] = names[i+1:]
  return out

def parseProfs(proffile):
  pf = open(proffile, "r")
  profs = pf.readlines()
  pf.close()
  profs = [p.rstrip().lstrip() for p in profs]
  profs = filter(lambda s: len(s) > 0 and not s.startswith('#'), profs)
  out = []
  for p in profs:
    l = p.split(", ")
    name = l.pop(0)
    maxtimes = int(l.pop(0))
    l = map(int, l)
    out.append((name, maxtimes, l))
  return out
    

def genHenches(numHenches, level, classes, market, al, spells, names, profs,gear,notabs=True):
  outlist = []
  for k in range(0,numHenches):
    stats=[]
    for i in range(0,6):
      acc = 0
      for j in range(0,3):
        acc+= random.randint(1,6)
      stats.append(acc)

    prefix = ""
    if market != 10:
      prefix = "\t"
    ostring = str(stats)

    if classes != []:
      cweights = []
      for c in classes:
        weight = min([f(stats) for f in c[2]])
        cweights.append((c[5] * weight, c))
      cweights = filter((lambda t: t[0] > 0),cweights)
      poss = []
      for (w,c) in cweights:
        for i in range(0,int(math.ceil(w))):
          poss.append(c)
      if len(poss) == 0:
        # if no possibilities, we default to first thing in list
        # generally fighter
        poss.append(classes[0])
      if level == 0:
        poss = [("Normal Man", 4, [], "", 0.5, 1.0)]
      ind = random.randint(0,len(poss)-1)
      hd = int(poss[ind][1])
      hp = max(random.randint(1,hd)+mod(stats[4]),1)
      if level > 1:
        for i in range(0,level-1):
          hp += max(random.randint(1,hd)+mod(stats[4]),1) 
      ostring += ", L" + str(level) + " " + poss[ind][0] + ", HP: " + str(hp)

    if names != []:
      g = float(poss[ind][4])
      g = 'M' if random.random() >= g else 'F'
      if g == 'F': ostring = ostring.replace('Man','Woman')
      ostring = names[g][random.randint(0,len(names[g])-1)] +" (" + g +"): " + ostring
      
    ostring = prefix + ostring

    if al:
      al = alignments[random.randint(1,6)-1]
      ostring += ", AL: " + al

    if profs != []:
      # build weightmap for this stat set
      weightmap = {}
      for p in profs:
        weight = -1 * 8**2 * len(p[2])
        if len(p[2]) == 0:
          weight = 3
        for c in p[2]:
          weight += (stats[c-1]) **2
        if weight > 0:
          weightmap[(p[0], p[1])] = weight
      weightlist = []
      for p in profs:
        t = (p[0], p[1])
        if t in weightmap.keys():
          for i in range(0, weightmap[t]):
            weightlist.append(t)
      profmap = {}
      bonusprofs = max(0, mod(stats[1]))
      if level == 0:
        # L0s get 4 unique profs plus possible dupes from int
        # have to account for the possibility of some poor bastard who quals for nothing
        while len(profmap.keys()) < min(4, len(weightmap.keys())):
          p = weightlist[random.randint(0, len(weightlist)-1)]
          profmap[p] = 1
      else:
        profmap[("Adventuring", 1)] = 1
        bonusprofs += (level-1)/4 +1
      for i in range(0, bonusprofs):
        done = False
        # 50% chance that we try to increase a prof we already have
        if random.random() < 0.5:
          profshave = profmap.keys()
          random.shuffle(profshave)
          for p in profshave:
            if profmap[p] < p[1]:
              profmap[p] += 1
              done = True
              break
        if not done:
          p = weightlist[random.randint(0, len(weightlist)-1)]
          while p[1] > 0 and p in profmap.keys() and profmap[p] >= p[1]:
            p = weightlist[random.randint(0, len(weightlist)-1)]
          if not p[0] in profmap.keys():
            profmap[p] = 1
          else:
            profmap[p] += 1
      profstrs = [ (p[0], profmap[p]) for p in profmap.keys()]
      acc = []
      for p in profstrs:
        if p[1] > 1:
          acc.append(p[0] + " " + str(p[1]))
        else:
          acc.append(p[0])
          
      profstr = ', '.join(sorted(acc))
      ostring += "\n\t" + prefix + "GenProfs: " + profstr

    if spells != [] and poss[ind][0].lower() in casters:
      mult = casters[poss[ind][0].lower()]
      ecl = int(math.floor(level * mult))
      if mult == 0.67 and level == 1:
        ecl = 1
      if ecl > 0:
        slist = libspellbook.genSpells(spells, ecl, mod(stats[1]), False)
        ostring += "\n\t" + prefix+"Spells known: "
        for i in range(0,len(slist)):
          ostring += "\t" +prefix + str(i+1) + ": " + ", ".join(slist[i])

    if level > 0 and gear:
      items = []
      for t in poss[ind][3]:
        if random.randint(1,20) <= level:
          try:
            items.append(tables.evaltable(itemtable[t]))
          except KeyError:
            print "No items for you on bad key: " + itemtable[t]
            gear = False
      istr = ", ".join(items)
      if istr != "":
        ostring += "\n\t" + prefix + "Gear: " + istr
    if notabs:
      ostring = re.sub('\t*','',ostring)
      ostring += '\n'
    outlist.append(ostring)
  return outlist

def genHenchesFiltered(fclass,numHenches, level, classes, market, al, spells, names, profs,gear,notabs=True):
  ol = genHenches(numHenches, level, classes, market, al, spells, names, profs, gear, notabs)
  if level == 0:
    return ol
  else:
    ol = filter(lambda s: fclass in s,ol)
    while len(ol) < numHenches:
      ol.extend(genHenches(numHenches-len(ol), level, classes, market, al, spells, names, profs, gear, notabs))
      ol = filter(lambda s:fclass in s,ol)
    return ol
