#!/usr/bin/env python3

import argparse
import math

# wages for stock mercenary types
merctypes = {
        "Light Infantry": 6,
        "Slingers": 6,
        "Heavy Infantry": 12,
        "Crossbowmen": 18,
        "Bowmen": 9,
        "Longbowmen": 18,
        "Light Cavalry": 30,
        "Horse Archers": 45,
        "Medium Cavalry": 45,
        "Heavy Cavalry": 60,
        "Cataphract Cavalry": 75,
  }

HEADER_LINE = ["Type", "I", "II", "III", "IV", "V", "VI"]

# Computes expected value of an entry for number of a type in a particular market class
def calc_ev(instr):
  ev = 1.0
  if ',' in instr:
    [instr,prob] = instr.split(',')
    ev *= float(prob)
  if 'd' in instr:
    [n,m] = instr.split('d')
    n = int(n)
    m = (int(m) + 1) * 0.5
    ev *= n * m
  else:
    n = int(instr)
    ev *= n
  return ev

# computes total value of mercenaries per month by for a given market class
def total_market_val(market_class, lines):
    total = 0
    for line in lines:
        instr = line[market_class]
        ev = calc_ev(instr)
        type_wage = merctypes[line[0]] * ev
        total += type_wage
    return total

# compute total gp val of mercs per month for each market class
def all_market_vals(path):
    infile=open(path,"r")
    lines = infile.readlines()
    infile.close()
    lines = [l for l in lines if not l.startswith("#")]
    lines = [l.lstrip().rstrip() for l in lines]
    lines = [l.split(":") for l in lines]
    lines = [l for l in lines if l[0] in merctypes]
    return [total_market_val(market, lines) for market in range(1,7)]

def print_raw(res_map):
    print(",".join(HEADER_LINE))
    for merc in res_map:
        counts = [("%0.2f" % c) for c in res_map[merc]]
        print("%s,%s" % (merc, ",".join(counts)))

def print_scale(res_map, usizes, scale=120.0):
    print(",".join(HEADER_LINE))
    for merc in res_map:
        out_list = []
        for count in res_map[merc]:
            egroups = count / (scale / usizes[merc])
            if egroups < 1:
                out_list.append("%d months"%(int(math.ceil(1/egroups))))
            else:
                out_list.append("%d per month"%(int(math.floor(egroups))))
        print("%s,%s" % (merc, ','.join(out_list)))


def main():
    parser = argparse.ArgumentParser(description="Generate number of available monomercs based on total value of mercs by market class")
    parser.add_argument("-f","--infile",default="./hireprices",help="File of stock mercs available by market")
    parser.add_argument("-r","--ratios",help="File of ratios between types in narrowed mercenary mix")
    args = parser.parse_args()

    market_totals = all_market_vals(args.infile)

    lines = open(args.ratios, 'r').readlines()
    lines = [l for l in lines if not l.startswith("#")]
    lines = [[s.rstrip().lstrip() for s in l.split(":")] for l in lines]
    types = [l[0].rstrip() for l in lines]
    total_parts = sum([float(l[1]) for l in lines])
    block_wage = sum([float(l[1]) * float(l[3]) for l in lines])
    print("Block wage: %0.2f" % block_wage)

    usize_map = {l[0]: int(l[2]) for l in lines}

    blocks_by_class = [tot / block_wage for tot in market_totals]

    res_map = {}

    for l in lines:
        res_arr = []
        for blocks in blocks_by_class:
            res_arr.append(blocks * float(l[1]))
        res_map[l[0]] = res_arr

    print("Raw counts")
    print_raw(res_map)

    scales = [
            ("Squad", 6),
            ("Platoon", 30),
            ("Company", 120),
            ]

    for (sname, scale) in scales:
        print("\n%s" % sname)
        print_scale(res_map, usize_map, scale=scale)
            

if __name__ == "__main__":
    main()
