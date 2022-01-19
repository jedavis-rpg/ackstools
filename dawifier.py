#!/usr/bin/env python2

import math
from ConfigParser import RawConfigParser
import sys
import glob

char_defaults = {
  'int': '0',
  'wis': '0',
  'cha': '0',
  'edmg_melee': '0',
  'edmg_ranged': '0',
  'no_melee_att': '1',
  'no_ranged_att': '1',
  'fighter_ml': '0',
  'max_arcane': '0',
  'max_divine': '0',
  'cleave_mult': '0',
  'command': '0',
  'leadership': '0',
  'milstrat': '0',
  'rof_ranged': 4,
  'rof_melee': 5
}

cleave_factors = {
  0:0,
  1: 0.35,
  2: 0.5,
  3: 0.65,
  4: 0.85,
  5: 1.1,
  6: 1.4,
  7: 1.75,
  8: 2.15,
  9: 2.7,
  10: 3.33,
  11: 4.15,
  12: 4.15,
  13: 4.15,
  14: 4.15,
  15: 4.15
}
  

fpath = sys.argv[1]
charconf = RawConfigParser(char_defaults)
charconf.read(fpath)

class Daw_Char(object):
  # a set of character stats at a given scale
  def __init__(self, scale, char):
    self.scale = scale.get('desc', 'name')
    self.can_cmd = char.getint('class', 'level') >= scale.getint('quals', 'min_cmd_lvl')
    self.can_lt = char.getint('class', 'level') >= scale.getint('quals', 'min_lt_lvl')
    self.can_hero = self.can_cmd
    self.can_hero |= char.getint('class', 'max_arcane') >= scale.getint('quals', 'min_arcane')
    self.can_hero |= char.getint('class', 'max_divine') >= scale.getint('quals', 'min_divine')
    mental_stats = [char.getint('stats', 'int'), char.getint('stats', 'wis'), 0]
    self.strat = max(mental_stats)+min(mental_stats)+char.getint('profs', 'milstrat')
    if self.can_cmd:
      self.ld = 4+char.getint('stats', 'cha')+char.getint('profs', 'leadership')
    else:
      self.ld = 0
    self.zoc = int(math.ceil(self.ld / 2.0))
    if self.can_lt:
      self.ml = char.getint('stats', 'cha')+2*char.getint('profs', 'command')
      if char.getint('class', 'fighter_ml') and char.getint('class', 'level') >= 5:
        self.ml += 1
    else:
      self.ml = 0 # TODO effects of attached independent heroes unqualified to be lieutenants on unit morale?
    # attack sequence
    self.attacks = {}
    for reach in ['melee', 'ranged']:
      edmg = char.getfloat('stats', 'edmg_%s'%reach)
      if edmg > 0:
        cleave_level = int(math.floor(char.getint('class', 'level') * char.getfloat('class', 'cleave_mult')))
        cleave_factor = min(cleave_factors[cleave_level], char.getint('stats', 'rof_%s'%reach))
        # TODO this rounding is not exactly to spec
        base_no_att = char.getint('stats', 'no_%s_att'%reach)
        no_attacks = int(round((base_no_att+cleave_factor) * edmg / scale.getfloat('math', 'dmg_divisor')))
        self.attacks[reach] = "%d@%d+"%(no_attacks, char.getint('stats', 'thaco_%s'%reach))
      else:
        self.attacks[reach] = "0"

  def output_as_list(self):
    return [self.scale, self.can_cmd, self.can_lt, self.can_hero, self.ld, self.zoc, self.strat, self.ml, self.attacks['melee'], self.attacks['ranged']]


scale_confs = []
for scale in glob.glob('./daw-scales/*'):
  scale_confs.append(RawConfigParser())
  scale_confs[-1].read(scale)
chars = [Daw_Char(sconf, charconf) for sconf in scale_confs]

cols = [c.output_as_list() for c in chars]
cols.sort(key=lambda x: x[0]) # sort alphabetically by scale name
header = ['Scale', 'Can Command?', 'Can LT?', 'Can hero?', 'LD', 'ZOC', 'Strat', 'ML', 'Melee', 'Ranged']
cols.insert(0,header)
rows = [[str(c[i]) for c in cols] for i in xrange(len(cols[0]))] # transpose
rows = ['| %s |'%(' | '.join(l)) for l in rows]
out = '| *DaW Stats:* |\n' + '\n'.join(rows)
print out
