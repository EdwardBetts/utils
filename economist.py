#!/usr/bin/python

# Copy the audio edition of the economist to an MP3 player
# The MP3 files are supplied in a zip file, it follows a standard naming 
# convention. MP3 files start with a three digit number to give sort order
# but the zip file is unordered. Some MP3 players don't sort, they need
# files to be copied in sorted order.

# This script assumes the economist zip is in ~/lib/economist
# Dates are parsed and the most recent zip file is used.

# Destination is the first mounted device that contains an economist directory
# Creates a dir with in a name in ISO format

from zipfile import ZipFile
from datetime import datetime, date
import os, re, sys

re_strip = re.compile('( \d+)(st|nd|rd|th) ')

te = 'The Economist '

dest = []
for i in os.listdir('/media'):
    if not os.path.isdir('/media/' + i):
        continue
    maybe = '/media/' + i + '/economist'
    if not os.path.exists(maybe):
        continue
    dest.append(maybe)
assert len(dest) == 1
dest = dest[0]

date_and_name = []

src = os.path.expanduser('~/lib/economist/')
for f in os.listdir(src):
    if not f.endswith('.zip'):
        continue
    assert f.startswith(te)
    d = re_strip.sub(lambda m:m.group(1) + ' ', f[len(te):-4])
    dt = datetime.strptime(d, '%B %d %Y').strftime('%Y-%m-%d')
    date_and_name.append((dt, f))

(dt, name) = max(date_and_name)

dest += '/' + dt
os.mkdir(dest)
zf = ZipFile(src + name, 'r')
for member in sorted(zf.namelist()):
    print member
    zf.extract(member, dest)
