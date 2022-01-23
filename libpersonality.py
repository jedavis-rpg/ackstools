#!/usr/bin/env python2

import random
import re

CLASSES = ["fighter", "cleric", "mu", "thief"]

class Trait(object):
  def __init__(self, name, classweights, excluded):
    self.name = name
    self.classweights = dict(zip(CLASSES, [float(w) for w in classweights]))
    self.excluded = set(excluded)

  def adj(self, strength):
    return self.strengths[strength-1]

  def __repr__(self):
    return "%s: %s, excludes %s"%(self.name, self.classweights, self.excluded)

class Virtue(Trait):
  def __init__(self, name, classweights, excluded):
    super(Virtue, self).__init__(name, classweights, excluded)
    self.strengths = [
      "rather",
      "very",
      "famously",
      "beatifically"
      ]

class Vice(Trait):
  def __init__(self, name, classweights, excluded):
    super(Vice, self).__init__(name, classweights, excluded)
    self.strengths = [
      "a little",
      "quite",
      "notoriously",
      "monstrously"
      ]

def parse_conf(confpath):
  lines = open(confpath, 'r').readlines()
  lines = [l.split('#')[0] for l in lines]
  lines = [l.rstrip().lstrip() for l in lines]
  lines = [l for l in lines if len(l)]
  assert lines.pop(0) == "virtues"
  virtues = []
  while lines[0] != "vices":
    l = lines.pop(0)
    parts = l.split(', ')
    traitname = parts[0]
    weights = parts[1:5]
    excluded = parts[5:]
    virt = Virtue(traitname, weights, excluded)
    virtues.append(virt)
  lines.pop(0) # get rid of vices
  vices = []
  while lines:
    l = lines.pop(0)
    parts = l.split(', ')
    vicename = parts[0]
    weights = parts[1:5]
    excluded = []
    for trait in virtues:
      if vicename in trait.excluded:
        excluded.append(trait.name)
    vice = Vice(vicename, weights, excluded)
    vices.append(vice)
  return {'virtue':virtues, 'vice':vices}


ROLL_RESULTS = {
  2: [(4, "vice"), (3, "vice"), (1, "virtue"), (2, "vice")],
  3: [(3, "vice"), (2, "vice"), (1, "virtue")],
  4: [(3, "vice"), (1, "vice"), (1, "virtue")],
  5: [(2, "vice"), (1, "virtue")],
  6: [(1, "virtue"), (1, "vice")],
  7: [(1, "vice"), (2, "virtue")],
  8: [(2, "virtue"), (1, "vice")],
  9: [(2, "virtue"), (1, "vice"), (1, "virtue")],
  10: [(3, "virtue"), (1, "virtue"), (1, "vice")],
  11: [(3, "virtue"), (2, "virtue"), (1, "vice")],
  12: [(4, "virtue"), (3, "virtue"), (1, "vice"), (2, "virtue")]
}

def gen_personality(traits, cls, wis, var):
  diesizes = [6, 6]
  if var:
    diesizes = [4, 8]
  roll = sum([random.randint(1,die) for die in diesizes])+wis
  if roll < 2:
    roll = 2
  if roll > 12:
    roll = 12
  tableres = ROLL_RESULTS[roll]
  pers = set()
  for (strength, traittype) in tableres:
    cantget = set()
    for (_, trait_had) in pers:
      cantget.add(trait_had.name)
      cantget |= trait_had.excluded
    poss_traits = [t for t in traits[traittype] if t.name not in cantget]
    total_weights = sum([t.classweights[cls] for t in poss_traits])
    idx = random.random() * total_weights
    while idx > poss_traits[0].classweights[cls]:
      idx -= poss_traits[0].classweights[cls]
      poss_traits.pop(0)
    chosen_trait = poss_traits[0]  
    pers.add((strength, chosen_trait))
  return ", ".join(["%s %s (+%d)"%(trait.adj(strength), trait.name, strength) for (strength, trait) in pers])
  
def gen_personality_nocls(traits_path, wis_mod, al):
    # totally different scheme here
    # Characters with +0 wis get 1 virtue and 1 vice
    # -3 Wis -> 3 vices, 0 virtues
    # -2 Wis -> 3 vices, 1 virtue
    # -1 Wis -> 2 vices, 1 virtue
    # etc up to
    # +3 Wis -> 3 virtues, 0 vices
    # Chaotic characters get vices instead of virtues for high wis
    num_virt_vice_map = {
            -3: (0, 3),
            -2: (1, 3),
            -1: (1, 2),
            0: (1, 1),
            1: (2, 1),
            2: (3, 1),
            3: (3, 0),
            }

    if al != "C":
        num_virtues, num_vices = num_virt_vice_map[wis_mod]
    else:
        num_vices, num_virtues = num_virt_vice_map[wis_mod]

    traits = parse_conf(traits_path)
    virtues = random.sample(traits["virtue"], num_virtues)
    excluded_set = reduce(lambda x,y:x.union(y), [v.excluded for v in virtues])
    potential_vices = [v for v in traits["vice"] if v.name not in excluded_set]
    vices = random.sample(potential_vices, num_vices)

    return {
            "virtues": sorted([v.name.capitalize() for v in virtues]),
            "vices": sorted([v.name.capitalize() for v in vices]),
    }
