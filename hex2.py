#!/usr/bin/python2

import random
# blah dice dependency
import dice
import argparse
import tables

random.seed()

# TODO move me to a data file
# the problem here is that the multitable function always joins with ', '
# if that were configurable, could join with '\n'
# and then have a table like CityStock: [CityEnc*2d4]
# but we don't, so we're doing it this way for now
lairdice = { "City": (1,4), "Inhabited":(1,4), "Clear":(1,4), "Grass":(1,4), "Scrub":(1,4),\
"Hills":(2,4,1), "Woods":(2,4,1), "Desert":(2,4,1), "Jungle":(2,6,1),\
"Mountain":(2,6,1), "Swamp":(2,6,1)}

parser = argparse.ArgumentParser(description="Stock hexes for ACKS")
parser.add_argument("-r","--rows",type=int,default=1,help="Number of rows of hexes to stock")
parser.add_argument("-c","--cols",type=int,default=1,help="Number of cols of hexes to stock")
parser.add_argument("-t","--terrain", default="Swamp",help="Terrain type to stock for")
parser.add_argument("-f","--terrainfile",default="./enctables",help="Name of terrainfile to stock from")
parser.add_argument("-m","--monsters",default="./monstertables",help="File of monsters to reference")
parser.add_argument("-e","--treasure", default="./treasuretables",help="File of treasure type tables")
parser.add_argument("-u","--full", action='store_true', help="Generate full lair/encounter descriptions")
parser.add_argument("-n","--encounter", action='store_true', help="Generate single encounter per hex rather than lairs")
args = parser.parse_args()

# load the monster file
tables.loadtables(args.monsters)
# load the terrain description
tables.loadtables(args.terrainfile)
# load the treasure files
tables.loadtables(args.treasure)

encTypeSuffix = "Enc" if args.encounter else "Lair"

# and now we generate the lairs in the hexes
for r in range(0,args.rows):
  for c in range(0,args.cols):
    if not args.encounter: print "Hex (" + str(r) + ", " + str(c) + "):"
    numlairs = 1 if args.encounter else dice.roll(lairdice[args.terrain])
    for i in range(0, numlairs):
      monster = tables.evaltable(args.terrain + "Enc")
      print monster
      monstertable = ''.join(monster.rstrip().lstrip().split(" ")) + encTypeSuffix
      if args.full and monstertable in tables.tabledice.keys():
        lairout = tables.evaltable(monstertable)
        print "\t" + lairout+"\n"
    print ""
