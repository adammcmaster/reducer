import astropy.io.fits

class FitsWrapper:
    hdu_list = []

    def __init__(self, filename=None):
        if filename:
            self.open(filename)

    def open(self, filename):
        self.hdu_list = astropy.io.fits.open(filename)

    def write(self, filename):
        hdu_out = astropy.io.fits.PrimaryHDU(
            self.combined_data,
            self.combined_headers
        )
        hdu_list_out = astropy.io.fits.HDUList([hdu_out])
        hdu_list_out.writeto(filename)
