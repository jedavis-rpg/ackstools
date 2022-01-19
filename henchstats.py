#!/usr/bin/python2
import argparse
import libhenches
import libspellbook
import tables
import sys

parser = argparse.ArgumentParser(description="Generate pile of stats for henches")
parser.add_argument("-n","--num",type=int,default=1,help="Number of henches to generate.\
  If market class is set, instead is number of months to generate henches for that market")
parser.add_argument("-c","--classes",default="",help="File to draw classes from")
parser.add_argument("-f","--filterclass",default="",help="Generate characters only of this class")
parser.add_argument("-m","--market",type=int, default=10,help="Market class value to use")
parser.add_argument("-a","--alignment",action="store_true",help="Generate alignments")
parser.add_argument("-s","--spells",default="",help="File to draw arcane spell list from")
parser.add_argument("-t","--treasure",default="",help="File to draw magic loot from")
parser.add_argument("-l", "--level",default=1,help="Generate NPCs of particular level")
parser.add_argument("--names",default="",help="File to draw NPC names from")
parser.add_argument("-g","--genprofs",default="",help="File to draw general profs from")
args = parser.parse_args()

classes = []
spells = []
names = []
profs = []
if len(args.classes) > 0:
  classes = libhenches.parseClasses(args.classes)
  if len(args.spells) > 0:
    spells = libspellbook.parseSpells(args.spells)
if len(args.names) > 0:
  names = libhenches.parseNames(args.names)
if args.treasure != "":
  tables.loadtables(args.treasure)
if args.genprofs != "":
  profs = libhenches.parseProfs(args.genprofs)

if args.filterclass:
  cl = [t[0] for t in classes]
  if args.filterclass not in cl:
    print "Class %s not found in class file (used same case?)"%args.filterclass
    sys.exit(1)


if args.market == 10:
  if args.filterclass:
    ol = libhenches.genHenchesFiltered(args.filterclass, args.num, int(args.level), classes, args.market, args.alignment, spells, names, profs, args.treasure != '')
  else:
    ol = libhenches.genHenches(args.num, int(args.level), classes, args.market, args.alignment, spells, names, profs, args.treasure != '')
  outstring = '\n'.join(ol)
  print outstring

else:
  for month in range(0,args.num):
    print "Month " + str(month) + ":"
    for level in range(0,5):
      numHenches = libhenches.rollMarket(libhenches.marketClasses[args.market-1][level])
      print "L" + str(level) + "s: " + str(numHenches)
      if args.filterclass:
        ol = libhenches.genHenchesFiltered(args.filterclass, numHenches,level, classes, args.market, args.alignment, spells, names, profs, args.treasure != '') 
      else:
        ol = libhenches.genHenches(numHenches, level, classes, args.market, args.alignment, spells, names, profs, args.treasure != '')
      outstring = '\n'.join(ol)
      print outstring
