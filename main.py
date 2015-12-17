#!/usr/bin/env python

import os
import tile

for filename in os.listdir('/data/'):
    if not filename.endswith('.fz'):
        continue

    t = tile.Tiler(os.path.join('/data', filename))
    t.tile()
    t.write(os.path.join('/data', filename.replace('.fits.fz', '_output.fits')))
