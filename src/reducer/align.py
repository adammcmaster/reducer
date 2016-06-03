import astropy.wcs

from reducer.fits import FitsWrapper

# Takes two FITS images and extends them to include each other's data ranges
# based on their WCS coordinates, but doesn't actually stack them.
class Aligner(FitsWrapper):
    def __init__(self, in_file=None):
        super(Aligner, self).__init__(in_file)

        # Ideally this should be self.header, but something is messed up in the
        # combined headers.
        self.wcs = astropy.wcs.WCS(self.hdu_list[0].header)

    # self and other will both be modified to extend them and shift their data
    # to the correct place
    def align(self, other):
        other = Aligner(other)
        other_origin = other.wcs.all_pix2world(0, 0, 0)
        self_origin = self.wcs.all_pix2world(0, 0, 0)

        self_origin_in_other = other.wcs.all_world2pix(
            self_origin[0],
            self_origin[1],
            0
        )
        other_origin_in_self = self.wcs.all_world2pix(
            other_origin[0],
            other_origin[1],
            0
        )

        print self_origin_in_other
        print other_origin_in_self

        # NEXT: Do something useful with this

    def _parse_coord(self, coord_string):
        pass
