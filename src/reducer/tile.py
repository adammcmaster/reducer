import numpy
import re

from reducer.fits import FitsWrapper

# Takes a mosaic FITS file and creates a flat image
class Tiler(FitsWrapper):
    combined_data = None

    def tile(self):
        detsize = self._parse_datarange(self.hdu_list[0].header['DETSIZE'])
        self.combined_data = self._mkndarray(detsize)
        map(self._add_hdu, self.hdu_list[1:])

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
        for in_row, out_row in zip(
            range(*data_range[1]),
            range(*combined_range[1])
        ):
            for in_col, out_col in zip(
                range(*data_range[0]),
                range(*combined_range[0])
            ):
                self.combined_data[out_row-1][out_col-1] = (
                    hdu.data[in_row-1][in_col-1]
                )

        self._combine_headers(hdu.header)

    # We want to keep any metadata fields that are the same for every HDU and
    # discard any that differ
    def _combine_headers(self, new_headers):
        excluded_headers = (
            'DETSIZE',
            'BIASSEC',
            'DATASEC'
        )
        for key, value in new_headers.items():
            if key in excluded_headers:
                continue

            if (
                key in self.header and
                self.header[key] != value
            ):
                del self.header[key]
            else:
                self.header.setdefault(key, value)
