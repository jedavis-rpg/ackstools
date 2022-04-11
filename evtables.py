#!/usr/bin/env python2

# library for calculating expected number of times certain "terminal" tables are called
# eg: If you have a wilderness encounter in a swamp, how many scrolls are you likely to find?
# This uses the data format described and parsed in tables.py

import re
import sys
import tables

"""
our acc state is something like a dict of terminal names to floats
when we "eval" a table, we're computing EV of calls to each terminal.
I think we can ignore plus, mult, and dice - we only care about
prob, table, and multitable.

Ed: not quite true, we need dicereg to be run before multitable, but we'll make it compute EV instead of rolling.

Table and multitable are easy.
Although we're going to need to modify multitable reg to handle decimals
for dice EV results.

Handling probability is trickier - we need a way to figure out the EVs
that *aren't* in the probability block.  But regex are too weak for this/
this wouldn't be context-free.

What we *can* do is compute the whole thing as if there were no probability blocks, and then subtract the "losses" from the probability blocks.
This might work as long as no prob blocks are nested.

I suspect that we have no nested probability blocks but I am not sure.

And indeed, the old table.py does not support handling of nested probability blocks as far as I can tell, as only a single pass of probreg is made over each entry.
"""

multitablereg_fl = re.compile('\[([a-zA-Z0-9]+)\*(\d+\.?\d*)\]')

def sum_dicts(a, b):
    out = {}
    for k in a:
        if k in b:
            out[k] = a[k]+b[k]
        else:
            out[k] = a[k]
    for k in b:
        if k not in out:
            out[k] = b[k]
    return out

def dict_mult_scalar(a, b):
    out = {}
    for k in a:
        out[k] = a[k] * b
    return out

def subdice_ev(match):
    return str(float(match.group(1)) * (float(match.group(2))+1.0)/2.0)
    
def process(entry, terminals):
    # replace dice with EVs first
    entry = tables.dicereg.sub(subdice_ev, entry)

    probs = tables.probreg.findall(entry)
    tabs = tables.tablereg.findall(entry)
    multitabs = multitablereg_fl.findall(entry)
    term_counts = {k:0.0 for k in terminals}

    for tab in tabs:
        term_counts = sum_dicts(term_counts, eval_table(tab, terminals))

    for multitab in multitabs:
        term_counts = sum_dicts(term_counts, dict_mult_scalar(eval_table(multitab[0], terminals), float(multitab[1])))

    prob_subs = {k:0.0 for k in terminals}
    for prob in probs:
        prob_subs = sum_dicts(prob_subs, dict_mult_scalar(process(prob[0], terminals), 1.0 - float(prob[1])))

    prob_subs = {k:-prob_subs[k] for k in prob_subs}

    term_counts = sum_dicts(term_counts, prob_subs)

    return term_counts


def build_probs_table(n, m):
    if n == 1:
        return [1 / float(m) for _ in xrange(m)]
    if n == 2:
        center = m+1
        # P(center) is always equal to 1/m
        # and each step of distance away from center reduces probability
        # by 1/m^2
        return [1.0 / m - abs(i-center) * (1.0 / m**2) for i in xrange(2, 2*m+1)]
    else:
        # TODO polynomial multiplication
        raise NotImplementedError


def eval_table(tablename, terminals):
    """
    we need to compute the probability of each entry on the table
    generate its expected terminal counts
    and then multiply those by its probability
    gross
    Can we exploit the monotonic structure of the tables?
    Current plan: special-case 1dn and 2dn
    and use generating functions for 3+dn
    """
    out = {k: 0.0 for k in terminals}

    if tablename in terminals:
        out[tablename] = 1.0
        return out

    numtoroll, diesize = tables.tabledice[tablename]
    probs = build_probs_table(int(numtoroll), int(diesize))
    l = tables.tableentries[tablename]
    idx_so_far = 0
    for i in xrange(len(l)):
        prob = sum(probs[idx_so_far:l[i][0]])
        idx_so_far = l[i][0]
        out = sum_dicts(out, dict_mult_scalar(process(l[i][1], terminals), prob))
    return out

def print_evs(tablename, evdict):
    out = tablename
    for k in sorted(evdict.keys()):
        out += "\n\t%s: %0.4f" % (k, evdict[k])
    print out

def main():
    terminals = ["Sword", "Potion", "Ring", "Scroll"]
    if len(sys.argv) < 2:
        print("Need an entrypoint table name")
    tables.loadtables("./treasuretables")
    tables.loadtables("./monstertables")
    for entry in sys.argv[1:]:
        print_evs(entry, eval_table(entry, terminals))

if __name__ == "__main__":
    main()
