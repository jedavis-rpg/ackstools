#!/usr/bin/python2

import re
import random
import argparse
import tables

parser = argparse.ArgumentParser(description="Generate treasure")
parser.add_argument("-t","--tables",default="./treasuretables",help=\
  "File containing list of treasure tables")
parser.add_argument("-n", "--num",type=int, default=1,help=\
  "Number to generate")
parser.add_argument("typelist",metavar='H',nargs='+',help=\
  "List of hoard types and tables to roll")
args = parser.parse_args()

tables.loadtables(args.tables)
for t in args.typelist:
  for i in range(0,args.num):
    print t + ": " + tables.evaltable(t)
