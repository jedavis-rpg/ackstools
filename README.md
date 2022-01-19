
ackstools

@jedavis-rpg

Python scripts for automating the annoying parts of DMing ACKS
These were all written for command-line use on linux
  TODO portablate

Scripts and supporting config files:

  demands.py - Generates demand modifiers for settlements
    (up to and including resolving effects of nearby markets on each other).
    Uses mercantmods.csv for the terrain and race modifiers.
    Uses a .towns file as its 'map' of the relative locations, ages, terrains
      (see shieldlands.towns for an example and format documentation).
    Uses dice.py because I'm an idiot sometimes (TODO remove dependency).

  dungeonrooms.py - Supply number of rooms, get numbers of 
    Empty, Trap, Monster, and Special rooms for dungeon stocking.
    Includes handling of empties with traps and treasure.
    No dependencies.

  hd.pl - perl script to roll a bunch of monster HD at once.
    I don't use this much anymore, instead preferring list comprehensions
    in a python interpreter session, but here for completeness.

  henchstats.py - Generates random henchmen for hire.
    Has a bunch of command line options, but in its fullest form,
    rolls stats, chooses an appropriate-ish class, gender, name, alignment,
    picks general proficiencies, generates random spells, and starting magic
    items (at the usual 5%/level NPC frequency).
    Can be driven by market class, or "give me 4 6th-level NPCs"; 
    therefore also useful for NPC party encounters.
    Uses classes, genprofs, spells, and treasuretables as data files.
    Uses libspellbook.py, libhenches.py, and tables.py as dependencies.

  hex2.py - Hex stocking and wilderness random encounter generation, v2
    Can generate fully-stocked lairs down to arbitrary detail.
    Has a bunch of command line options, consult --help for details.
    Deciding on the correct depth/detail to generate needs some work,
    as does formatting the outputs nicely
    (Currently full-detail humanoid lairs are really ugly).
    That's really a question of modifying monstertables, though.
    monstertables is a mapping from monster type to number encountered/treasure
    enctables is a transcription of the wilderness tables from pages 244-247.
    Uses treasuretables, monstertables, and enctables as data files.
    Uses dice.py, tables.py as dependencies.

  hirelings.py - How many mercenaries are available in town this month?
    Uses hireprices as a data file.

  magicavail.py - What magic items are available in town this month?
    Uses magicprices as a data file.

  markovnamegen.py - Generates random names by recombining inputs with Markov
    chains.  No data files provided (TODO).

  spellbook.py - Generate NPC mage's known spells.
    Uses libspellbook.py as dependency.
    Uses spells as a data file.

  tables.py - This is actually a library for handling a random table
    specification format I built and have been extending as needed.  
    See treasuretables and monstertables for examples/documentation.

  treasuregen.py - Generates treasure hoards.
    Uses tables.py as dependency.
    Uses treasuretables as a data file.
