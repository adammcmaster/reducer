#!/usr/bin/env python

import os
import progressbar
from reducer import tile, stack

files = []

bar = progressbar.ProgressBar()
# Flatten mosaics
print "Loading and flattening files..."
for filename in bar(os.listdir('/data/')):
    if not filename.endswith('.fz'):
        continue

    t = tile.Tiler(os.path.join('/data', filename))
    t.tile()
    files.append(t)

# Stack everything
s = stack.Stacker(files[0])
bar = progressbar.ProgressBar()
print "Stacking files..."
for f in bar(files[1:]):
    s.stack(f)

s.write(os.path.join('/', 'data', 'out', 'result.fits'))
