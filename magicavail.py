#!/usr/bin/python2

import random
import argparse

random.seed()

marketProbs = [[(0,1),1700,585,260,65,30,10],\
[(2,10),100,30,15,5,1,1],\
[(11,100),15,5,2,1,0.25,0.1],\
[(101,1000),7,2,1,0.25,0.1,0.05],\
[(1001,10000),2,1,0.25,0.1,0.05,0.01],\
[(10000,1000000000),0.1,0.05,0.02,0,0,0]]

def getnum(marketclass, price, numMonths):
  for l in marketProbs:
    if price>=l[0][0] and price <= l[0][1]:
      num = l[marketclass]
      if 0 < num and 1 > num:
        out = 0
        for i in range(0,numMonths):
          if random.random() < num:
            out = out +1
        return out
      else:
        return num*numMonths

def doLine(marketclass, item, price, numMonths, double):
  # derp the items file contains prices to create which are half sale prices
  if not double: price = 2*price
  num = getnum(marketclass, price, numMonths)
  if num > 0:
    print item + ": " + str(num) + " @ " + str(price) + "gp"

parser = argparse.ArgumentParser(description="Generate magic items avail in town")
parser.add_argument("-m","--market",type=int, default=4,help="Market class to gen for")
parser.add_argument("-f","--inFile",default="./magicprices",help="File of item prices")
parser.add_argument("-n","--numMonths",type=int,default=1,help="Number of months to gen for")
parser.add_argument("-d","--double",action="store_true",help="Don't double prices; used for nonmagic item generation")
args = parser.parse_args()

infile = open(args.inFile,"r")
lines = infile.readlines()
infile.close()
lines = filter(lambda s: not s.startswith('#'), lines)
lines = map(lambda k: k.lstrip().rstrip(), lines)
lines = map(lambda k: k.split(":"), lines)

map(lambda l: doLine(args.market, l[0],int(l[1]), args.numMonths,args.double), lines)
