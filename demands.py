#!/usr/bin/python2
# The purpose of this file is to generate demand mods for towns
# using the full trade routes rules and shit
# Currently takes a file of towns and potential trade links,
# generates base and terrain demands, and does dependency resolution
# to figure out routes.
# Thus, generates demand mods for an entire region from scratch
# TODO ability to load and save base mods before routing
# (for purposes of adding, removing, upgrading, or downgrading a link of market)
# TODO ability to generate / regenerate just one town
# TODO ability to write results straight to file (-o basically)
# TODO improve output formatting

import random
import dice
# for selRandFromList
import libspellbook
import copy
import argparse
random.seed()

# Maximum distance in hexes for purposes of Djikstra's alg for routing
MAXDIST = 10000000
# trade route ranges by market class
# in six-mile hexes
roadRange = [0, 28, 24, 18, 12, 8, 4]
waterRange = [0, 80, 60, 40, 20, 16, 8]
# number of positive and negative mods by land value
modsByLV = {\
  3:(6,1), 4:(4,1), 5:(2,1), 6:(1,1), 7:(1,2), 8:(1,4),9:(1,6)}


# Djikstra's algorithm to find shortest paths from source
# to each other connected settlement.
# Used by doRoutes to generate possible trade routes
def djik(source, dists):
  unvisited = copy.deepcopy(dists.keys())
  ests = {}
  for t in unvisited:
    if t == source:
      ests[t] = 0
    else:
      ests[t] = MAXDIST
  curr = source
  done = False
  while not done:
    for (t,d) in dists[curr]:
      if t in unvisited:
        if d+ests[curr] < ests[t]:
          ests[t] = d + ests[curr]
    unvisited.remove(curr)
    nextCurr = ""
    nextDist = MAXDIST
    for t in unvisited:
      if ests[t] < nextDist:
        nextDist = ests[t]
        nextCurr = t
    if nextDist == MAXDIST:
      done = True
    else:
      curr = nextCurr
  ret = dists.keys()
  ret.remove(source)
  ret = filter(lambda x: ests[x] < MAXDIST, ret)
  return map(lambda x: (x, ests[x]), ret)


# Performs demand modifications for trade routes
# Params:
#   classes - map of town names to market class numbers
#   roadEdges - map of town names to (townName,distance) pairs for road links
#   waterEdges - as roadEdges, but for water links
#   demands - map of town names to maps of goodnames to demand modifiers
# Performs modifications in-place on the demands map, returns void
# Basically, iterates across set of towns, generates distances by road and
# water to each other town.  Cuts links that are too long for market classes,
# then sorts links by distance and min market class of the pair.
# Applies the effects of the dependencies in order of ascending market class
# and descending distance
def doRoutes(classes, roadEdges, waterEdges, demands):
  deps = []
  for s in classes.keys():
    roadPos = djik(s, roadEdges)
    waterPos = djik(s, waterEdges)
    # filter out the waypoints and markets too far
    roadDeps = filter(lambda (t,d): t in classes.keys(), roadPos)
    roadDeps = filter(lambda (t,d): d <= roadRange[max(classes[s], classes[t])],roadDeps)
    waterDeps = filter(lambda (t,d): t in classes.keys(), waterPos)
    waterDeps = filter(lambda (t,d): d <= waterRange[max(classes[s], classes[t])],waterDeps)
    roadDeps.extend(waterDeps)
    subDeps = map(lambda (t,d): (min(classes[s], classes[t]), d, s, t), roadDeps)
    deps.extend(subDeps)
  # sort by distance, then by minMarket
  # this is sweet, because python buitin sorts are stable
  # gives nearby things right of first influence
  # ...  actually, we want to apply nearby things last I think
  # weird emergent property of the system
  deps.sort(key=lambda t: t[1], reverse=True)
  deps.sort(key=lambda t: t[0])
  # we no longer need distance
  deps = map(lambda (v, d, s, t): (v, s, t), deps)
  seen = []
  # we track current market val for updating seen; start it too high, then drop in loop
  currMarket = 8
  while deps != []:
    (v,s,d) = deps.pop(0)
    # this one only triggers on first iteration; gets lowest market with deps
    if (currMarket > v):
      currMarket = v
    # this one is true if we've passed a market class threshold
    if (currMarket < v):
      seen = []
      currMarket = v
    # make sure we haven't already looked at this pair's inversion
    if (v,d,s) in seen:
      continue
    if classes[s] == classes[d]:
      for k in demands[s]:
        if demands[s][k] <= demands[d][k]-2:
          demands[s][k] +=1
          demands[d][k] -=1
        elif demands[s][k] -2 >= demands[d][k]:
          demands[s][k] -=1
          demands[d][k] +=1
        else:
          # you know what?  I'm ok with .5s in my demand mods
          tmp = min(demands[s][k], demands[d][k]) + 0.5
          demands[s][k] = tmp
          demands[d][k] = tmp
    else:
      tmpList = sorted(map (lambda x: (x, classes[x]), [s, d]), key=lambda t:t[1])
      strong = tmpList[0][0]
      weak = tmpList[1][0]
      for k in demands[s].keys():
        if demands[weak][k] < demands[strong][k]:
          demands[weak][k] = min(demands[strong][k], demands[weak][k]+2)
        else:
          demands[weak][k] = max(demands[strong][k], demands[weak][k]-2)
    seen.append((v,s,d))

# Loads the list of towns and routes from a file
# For a sample, see shieldland.towns
def parseMap(infilename):
  fdesc = open(infilename, 'r')
  lines = fdesc.readlines()
  fdesc.close()
  lines = filter(lambda s: not s.startswith('#'), lines)
  lines = map(lambda k: k.lstrip().rstrip(), lines)
  lines = map(lambda k: k.split(', '), lines)
  # assumption: at least one town.  Srsly.
  towns = []
  waypoints = []
  while lines[0] != ['']:
    t = lines[0]
    if len(t) > 2:  
      # t[0] is town name
      # t[1] is market class
      # t[2] is domain land value per family (3-9)
      # t[3] is string of terrain and age descriptors, space-separated
      # generate unknown domain land values
      if (t[2] == 'R'):
        t[2] = dice.roll((3,3))
        print t[0] + " land value " + str(t[2])
      else:
        t[2] = int(t[2])
      t[1] = int(t[1])
      towns.append(t)
    else:
      waypoints.append(t)
    lines.pop(0)
  # get rid of the blank line
  lines.pop(0)
  # and now we parse the road and water links
  roadMap = {}
  waterMap = {}
  for t in towns:
    roadMap[t[0]] = []
    waterMap[t[0]] = []
  for w in waypoints:
    roadMap[w[0]] = []
    waterMap[w[0]] = []
  while lines != []:
    # first two fields are town names, third is dist, fourth is link type
    link = lines[0]
    currMap = roadMap
    if (link[3] == 'W'):
      currMap = waterMap
    # all edges are symmetric; maps without this property would be interesting
    # cataracts on the river?
    currMap[link[0]].append((link[1],int(link[2])))
    currMap[link[1]].append((link[0],int(link[2])))
    lines.pop(0)
  return (towns, roadMap, waterMap)

# loads the CSV file of mods by good and terrain type
# many thanks to cmarteta from the forums for transcribing these
# currently lives in mercantmods.csv
def parseMods(modfilename):
  fdesc = open(modfilename, 'r')
  lines = fdesc.readlines()
  fdesc.close()
  lines = filter(lambda s: not s.startswith('#'), lines)
  lines = map(lambda k: k.lstrip().rstrip(), lines)
  lines = map(lambda k: k.split(':'), lines)
  indices = {}
  nextIndex = 0
  for desc in lines[0]:
    indices[desc] = nextIndex
    nextIndex+=1
  lines.pop(0)
  mods = {}
  nameslist = [good[0] for good in lines]
  for good in lines:
    name = good.pop(0)
    mods[name] = map(lambda x: float(x),good)
  return (indices, mods, nameslist)

# loads a supplementary, campaign-specific csv of mods
# and merges with standard array of mods
# modifies in place, returns void
def addMods(suppfilename,indices,mods):
  fdesc = open(suppfilename, 'r')
  lines = fdesc.readlines()
  fdesc.close()
  lines = filter(lambda s: not s.startswith('#'), lines)
  lines = map(lambda k: k.lstrip().rstrip(), lines)
  lines = map(lambda k: k.split(':'), lines)
  nextIndex = len(indices.keys())
  for desc in lines[0]:
    indices[desc] = nextIndex
    nextIndex+=1
  lines.pop(0)
  for good in lines:
    name = good.pop(0)
    mods[name].extend(map(lambda x: float(x),good))

# rolls base demands for each town, applies terrain and land value mods
def genDemands(towns, indices, mods):
  demands = {}
  for t in towns:
    demands[t[0]] = {}
    descs = t[3].split(' ')
    inds = map(lambda k: indices[k], descs)
    for k in mods.keys():
      tmp = random.randint(1,3) - random.randint(1,3) 
      for i in inds:
        tmp += mods[k][i]
      demands[t[0]][k] = tmp
    # handle the +/- mods by land value 
    (plus, minus) = modsByLV[int(t[2])]
    plusses = libspellbook.selRandFromList(plus, mods.keys())
    minuses = libspellbook.selRandFromList(minus, mods.keys())
    for k in plusses:
      demands[t[0]][k]+=1
    for k in minuses:
      demands[t[0]][k]-=1
  return demands

# does errything; loads from files, generates basic demands, resolves routes
def wholeSchebang(townsfile, modsfile,suppfile):
  (indices, mods, goodnames) = parseMods(modsfile)
  # TODO add support for multiple suppfiles
  if suppfile:
    addMods(suppfile, indices,mods)
  print indices
  (towns, roadMap, waterMap) = parseMap(townsfile)
  demands = genDemands(towns,indices,mods)
  classes = {}
  for t in towns:
    classes[t[0]] = t[1]
  doRoutes(classes,roadMap,waterMap,demands)
  return (demands, goodnames)

# TODO improve this shit so it prints in some sort of coherent order
def printDemands(demands, goodnames):
  for t in demands.keys():
    print t
    for k in names:
      print "\t" + k + ": " + str(demands[t][k])
    print ""

parser = argparse.ArgumentParser(description="Generate demand modifiers for ACKS region")
parser.add_argument("-t","--towns",default="",help="File containing towns and roads")
parser.add_argument("-m","--mods",default="./mercantmods.csv",help="csv file of demand modifiers by terrain and good types")
parser.add_argument("-s","--supp",default="",help="csv containing supplementary demand modifier columns")
args = parser.parse_args()

demands, names = wholeSchebang(args.towns, args.mods, args.supp)
printDemands(demands,names)
