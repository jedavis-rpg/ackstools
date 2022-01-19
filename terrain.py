#!/usr/bin/env python2

import random

header = ['Terrain', 'Pieces', 'Broken', 'Cliff', 'Forest', 'Hills', 'Impenetrable Forest', 'Mud', 'Lake', 'Stream', 'Swamp', 'Trench']

terrlines = ['Clear,2d4,4,6,8,14,0,16,18,19,20,0\n', 'Grass,2d4,4,6,8,14,0,16,18,19,20,0\n', 'Barren,3d4,7,12,0,18,0,19,0,0,0,20\n', 'Desert,3d4,5,10,0,16,0,18,0,0,0,20\n', 'Hills,4d4,2,4,6,16,0,0,18,20,0,0\n', 'Scrub,4d4,2,4,8,16,17,0,18,19,0,20\n', 'Woods,4d6,2,4,12,14,17,0,18,19,20,0\n', 'Mountains,4d8,4,10,12,14,16,0,18,19,0,20\n', 'Jungle,4d8,0,2,10,12,15,16,17,19,20,0\n', 'Swamp,4d8,0,0,4,0,8,10,11,13,20,0\n']

def build_terrmap():
  terrmap = {}
  for l in terrlines:
    l = l.rstrip()
    parts = l.split(',')
    terrtype = parts.pop(0)
    num_pieces = parts.pop(0)
    probs = [int(x) for x in parts]
    terrmap[terrtype] = (num_pieces, probs)
  print terrmap
  return terrmap

terrmap = {'Mountains': ('4d8', [4, 10, 12, 14, 16, 0, 18, 19, 0, 20]), 'Scrub': ('4d4', [2, 4, 8, 16, 17, 0, 18, 19, 0, 20]), 'Hills': ('4d4', [2, 4, 6, 16, 0, 0, 18, 20, 0, 0]), 'Clear': ('2d4', [4, 6, 8, 14, 0, 16, 18, 19, 20, 0]), 'Swamp': ('4d8', [0, 0, 4, 0, 8, 10, 11, 13, 20, 0]), 'Woods': ('4d6', [2, 4, 12, 14, 17, 0, 18, 19, 20, 0]), 'Jungle': ('4d8', [0, 2, 10, 12, 15, 16, 17, 19, 20, 0]), 'Barren': ('3d4', [7, 12, 0, 18, 0, 19, 0, 0, 0, 20]), 'Grass': ('2d4', [4, 6, 8, 14, 0, 16, 18, 19, 20, 0]), 'Desert': ('3d4', [5, 10, 0, 16, 0, 18, 0, 0, 0, 20])}

def gen_terrain(terrtype):
  if not terrtype in terrmap:
    return []
  (piece_dice, probs) = terrmap[terrtype]
  [num_dice, die_size] = [int(x) for x in piece_dice.split('d')]
  print "Num dice: %d.  Die size: %d"%(num_dice, die_size)
  num_pieces = sum([random.randint(1,die_size) for _ in xrange(num_dice)])
  resmap = {}
  for _ in xrange(num_pieces):
    roll = random.randint(1,20)
    print roll
    for i in xrange(len(probs)):
      if roll <= probs[i]:
        piece_type = header[i+2]
        if piece_type not in resmap:
          resmap[piece_type] = 0
        resmap[piece_type] += 1
        break
  return [(k, resmap[k]) for k in sorted(resmap.keys())]
