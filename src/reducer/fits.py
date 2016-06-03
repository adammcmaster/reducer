import astropy.io.fits
import numpy
import re

# Wrapper around astropy's FITS class. Can be initialised with the filename of
# a FITS file, or with another FitsWrapper object.
class FitsWrapper(object):
    excluded_headers = [
        'DETSIZE',
        'BIASSEC',
        'DATASEC'
    ]

    def __init__(self, in_file=None):
        if in_file:
            if isinstance(in_file, FitsWrapper):
                self.hdu_list = astropy.io.fits.HDUList(in_file.hdu_list)
                self.header = astropy.io.fits.Header(in_file.header)
                self.original_filename = in_file.original_filename
            else:
                self.original_filename = in_file
                self.open(in_file)

    def open(self, filename):
        self.hdu_list = astropy.io.fits.open(filename)
        self.header = self.hdu_list[0].header.copy()

    def write(self, filename):
        self.hdu_list.writeto(filename)

    def _parse_datarange(self, range_string):
        m = re.match(
            (r'\[(?P<x_start>[0-9]+):(?P<x_end>[0-9]+),\s*'
             '(?P<y_start>[0-9]+):(?P<y_end>[0-9]+)\]'),
            range_string
        )

        if not m:
            raise Exception('Could not parse data range "%s"' % range_string)

        return (
            (int(m.group('x_start')), int(m.group('x_end'))),
            (int(m.group('y_start')), int(m.group('y_end')))
        )

    def _mkndarray(self, ranges):
        return numpy.ndarray(
            shape=(
                ranges[1][1] - ranges[1][0],
                ranges[0][1] - ranges[0][0]
            )
        )

    # We want to keep any metadata fields that are the same for every HDU and
    # discard any that differ
    def _combine_headers(self, new_headers):
        for key, value in new_headers.items():
            if key in self.excluded_headers:
                continue

            if (
                key in self.header and
                self.header[key] != value
            ):
                del self.header[key]
                self.excluded_headers.append(key)
            else:
                self.header.setdefault(key, value)
