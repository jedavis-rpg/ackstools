#!/usr/bin/env python2

import argparse
import libhenches
import libpersonality
import random

def main():
  parser = argparse.ArgumentParser(description="Generate personality traits for NPCs")
  parser.add_argument("-c", "--cls", default="fighter",help="fighter, cleric, mu, or thief")
  parser.add_argument("-n", "--num", type=int, default=1,help="Number of personalities to generate")
  parser.add_argument("-w", "--wis", type=int, default=0,help="Wisdom modifier")
  parser.add_argument("-v", "--var", action="store_true",help="Use high variance morality generator")
  parser.add_argument("-r", "--rand_wis", action="store_true",help="Generate random wisdom score")
  parser.add_argument("--conf", default="./ptraits", help="Path to config file")
  args = parser.parse_args()
  if args.cls not in CLASSES:
    print "cls argument must be one of %s"%CLASSES
    return -1
  traitmap = parse_conf(args.conf)

  for i in xrange(args.num):
    if args.rand_wis:
      wis_score = sum([random.randint(1,6) for _ in xrange(3)])
      print "Wisdom: %d"%wis_score
      wis = libhenches.mod(wis_score)
    else:
      wis = args.wis
    print libpersonality.gen_personality(traitmap, args.cls, wis, args.var)


if __name__ == "__main__":
  main()
