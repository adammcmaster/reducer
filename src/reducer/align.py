from reducer.fits import FitsWrapper

# Takes two FITS images and extends them to include each other's data ranges
# based on their WCS coordinates, but doesn't actually stack them.
class Aligner(FitsWrapper):
    ra = None
    dec = None

    def __init__(self, in_file=None):
        super(Aligner, self).__init__(in_file)

        self.ra = self._parse_coord(self.header['RA'])
        self.dec = self._parse_coord(self.header['DEC'])

    # self and other will both be modified to extend them and shift their data
    # to the correct place
    def align(self, other):
        pass

    def _parse_coord(self, coord_string):
        pass
