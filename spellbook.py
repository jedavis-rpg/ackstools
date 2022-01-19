#!/usr/bin/python2
import libspellbook
import argparse

parser = argparse.ArgumentParser(description="Generate spellbooks for ACKS wizards")
parser.add_argument("-n","--num",type=int,default=1,help="Number of spellbooks to generate")
parser.add_argument("-l","--level",type=int,default=1,help="Level of mage to generate for")
parser.add_argument("-s","--spells",default="./spells",help="File to draw spells from")
parser.add_argument("-i","--intel", type=int,default=1,help="Intelligence bonus of mage")
parser.add_argument("-e","--excess",action="store_true",help="Allow mages to know spells\
  beyond the limits of their repertoire, as PC mages are wont to do")
args = parser.parse_args()

spells = libspellbook.parseSpells(args.spells)

for i in range(0,args.num):
  known = libspellbook.genSpells(spells, args.level, args.intel, args.excess)
  libspellbook.printSpells(known)
