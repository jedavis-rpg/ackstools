#!/usr/bin/env python2

import argparse

def main():
  parser = argparse.ArgumentParser(description="Compute XP and GP shares for party members")
  parser.add_argument("-pcs",default=3,type=int,help="Number of PCs")
  parser.add_argument("-henches",default=3,type=int,help="Number of henchmen")
  parser.add_argument("-gp",default=0,type=int,help="GP recovered")
  parser.add_argument("-xp",default=0,type=int,help="XP earned from monsters")
  args = parser.parse_args()

  total_xp = args.gp+args.xp
  pc_base_xp_share = total_xp / (args.pcs+args.henches/2.0)
  for i in xrange(5):
    print "PC XP at +%d%%: %d"%(5*i, round(pc_base_xp_share * (1+0.05*i), 1))
  for i in xrange(5):
    print "Hench XP at +%d%%: %d"%(5*i, round(pc_base_xp_share * (1+0.05*i)/2.0, 1))
  print "PC GP share: %d"%(round(args.gp / (args.pcs + args.henches / 6.0), 2))

if __name__ == "__main__":
  main()
