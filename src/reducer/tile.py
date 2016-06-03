import astropy.io.fits

from reducer.fits import FitsWrapper

# Takes a mosaic FITS file and creates a flat image
class Tiler(FitsWrapper):
    def tile(self):
        detsize = self._parse_datarange(self.hdu_list[0].header['DETSIZE'])
        self.combined_data = self._mkndarray(detsize)

        map(self.add_hdu, self.hdu_list[1:])
        hdu_out = astropy.io.fits.PrimaryHDU(
            self.combined_data,
            self.header
        )
        self.hdu_list = astropy.io.fits.HDUList([hdu_out])

    def add_hdu(self, hdu):
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
