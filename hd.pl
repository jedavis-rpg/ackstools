#!/usr/bin/perl

local $i = 0;
local $reps=1;
if (@ARGV > 1)
{
  $reps = int($ARGV[1]);
}
local $size = 8;
if (@ARGV > 2)
{
  $size = $ARGV[2];
}
local $numhd = int($ARGV[0]);
while($i < $reps)
{
  if ($i != 0) {print ", ";}
  local $hp = 0;
  local $j = 0;
  while($j < $numhd)
  {
    $hp += int(rand($size)+1);
    $j++;
  }
  print $hp;
  $i++;
}
print "\n";
