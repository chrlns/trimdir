#!/usr/bin/python

# This little script was written by Christian Lins <christian.lins@web.de>
# and is hereby released as Public Domain.
# If you have corrections for this script, please write me :-)
# What does this script? It trims the size of a directory (e.g. your desktop trash) 
# under a specific treshold by deleting old files.
# Please note: this script does not work on Windows platforms.

import os
from os import *
from os.path import *
import sys

# Path of the directory that should be trimmed
PATH = None 

# Maximum size of trash in megabyte
MAXSIZE   = 1024   

# Determines the size of the given directory recursing all subdirs
def dirsize(size, path):
  for root, dirs, files in os.walk(path):
    for name in files:
      joinedpath = join(root, name)
      if not islink(joinedpath):
        size += getsize(joinedpath)
  return size

# Removes a directory and all containing files and subdirectories
def rmdir_r(path):
  try:
    allin = listdir(path)
    for df in allin:
      if isfile(path + "/" + df) or islink(path + "/" + df):
        remove(path + '/' + df)
      else:
        rmdir_r(path + '/' + df)
    if path.startswith(PATH):
      rmdir(path)
    else:
      print "Sanity check failed!"
  except OSError, ex:
    print "Error while deleting %s: %s" % (path, ex)

def regtrash():
  current_size = dirsize(0, PATH) / 1024 / 1024
  filetimes = {}

  for f in listdir(PATH):
    if not islink(PATH + '/' + f):
      filetimes[getatime(PATH + '/' + f)] = f
    else:
      unlink(PATH + '/' + f)
  
  while current_size > MAXSIZE and len(filetimes) > 0:
    print "Trash has size if %u megabytes." % current_size
    # Search for smallest time value
    smallest = filetimes.keys()[0]
    for ftime in filetimes:
      if smallest > ftime:
        smallest = ftime
    delpath = PATH + "/" + filetimes[smallest]
    print "Purging " + delpath + " .."
    del filetimes[smallest]
    if isdir(delpath):
      current_size -= dirsize(0, delpath)
      rmdir_r(delpath)
    else:
      current_size -= getsize(delpath) / 1024 / 1024
      if delpath.startswith(PATH):
        remove(delpath)
      else:
        print "Sanity check failed!"

# Check for command line parameter
if len(sys.argv) != 2 and len(sys.argv) != 3:
  print "Usage: trimdir.py <directory> [maxsize in megabyte]\n"
  sys.exit(1)
else:
  PATH = sys.argv[1]
  if len(sys.argv) == 3:
    MAXSIZE = int(sys.argv[2])
  regtrash()
  sys.exit(0)

