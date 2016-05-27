#!/usr/bin/env python

import os
from reducer import tile, stack

files = []

# Flatten mosaics
for filename in os.listdir('/data/'):
    if not filename.endswith('.fz'):
        continue

    t = tile.Tiler(os.path.join('/data', filename))
    t.tile()
    files.append(t)

# Stack everything
s = stack.Stacker(files[0])
map(s.stack, files[1:])

s.write(os.path.join('/', 'data', 'out', 'result.fits'))
