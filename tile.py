import astropy.io.fits
import numpy
import re

class Tiler:
    hdu_list = []
    combined_data = None

    def __init__(self, filename=None):
        if filename:
            self.open(filename)

    def open(self, filename):
        self.hdu_list = astropy.io.fits.open(filename)

    def tile(self):
        detsize = self._parse_datarange(self.hdu_list[0].header['DETSIZE'])
        self.combined_data = self._mkndarray(detsize)
        map(self._add_hdu, self.hdu_list[1:])

    def write(self, filename):
        hdu_out = astropy.io.fits.PrimaryHDU(self.combined_data)
        hdu_list_out = astropy.io.fits.HDUList([hdu_out])
        hdu_list_out.writeto(filename)

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

    def _add_hdu(self, hdu):
        data_range = self._parse_datarange(hdu.header['DATASEC'])
        combined_range = self._parse_datarange(hdu.header['DETSEC'])
        for in_row, out_row in zip(range(*data_range[1]), range(*combined_range[1])):
            for in_col, out_col in zip(range(*data_range[0]), range(*combined_range[0])):
                self.combined_data[out_row-1][out_col-1] = hdu.data[in_row-1][in_col-1]
