import astropy.io.fits

# Wrapper around astropy's FITS class. Can be initialised with the filename of
# a FITS file, or with another FitsWrapper object.
class FitsWrapper:
    hdu_list = []
    header = astropy.io.fits.Header()

    def __init__(self, in_file=None):
        if in_file:
            if isinstance(in_file, FitsWrapper):
                self.hdu_list = list(in_file.hdu_list)
            else:
                self.open(in_file)

    def open(self, filename):
        self.hdu_list = astropy.io.fits.open(filename)
        self.header = self.hdu_list[0].header.copy()

    def write(self, filename):
        hdu_out = astropy.io.fits.PrimaryHDU(
            self.combined_data,
            self.combined_headers
        )
        hdu_list_out = astropy.io.fits.HDUList([hdu_out])
        hdu_list_out.writeto(filename)
