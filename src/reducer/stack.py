import astropy.wcs
import numpy
import traceback

from reducer.fits import FitsWrapper

# Takes two FITS images and stacks them (summing their pixel values)
class Stacker(FitsWrapper):
    aligner = None

    def __init__(self, in_file=None):
        super(Stacker, self).__init__(in_file)

    def stack(self, other):
        try:
            self_wcs = astropy.wcs.WCS(self.header)
        except ValueError:
            traceback.print_exc()
            print "Encountered error stacking {} onto {}. Skipping.".format(
                other.original_filename,
                self.original_filename
            )
            return

        self_origin_wcs = self_wcs.all_pix2world(0, 0, 0)
        data = self.hdu_list[0].data
        self_end_pix = (
            len(data),
            len(data[0])
        )
        self_end_wcs = self_wcs.all_pix2world(
            self_end_pix[0],
            self_end_pix[1],
            0
        )

        other_wcs = astropy.wcs.WCS(other.header)
        other_origin_wcs = other_wcs.all_pix2world(0, 0, 0)
        other_end_pix = (
            len(other.combined_data),
            len(other.combined_data[1])
        )
        other_end_wcs = other_wcs.all_pix2world(
            other_end_pix[0],
            other_end_pix[1],
            0
        )

        new_origin_wcs = (
            min(self_origin_wcs[0], other_origin_wcs[0]),
            min(self_origin_wcs[1], other_origin_wcs[1])
        )
        new_end_wcs = (
            max(self_end_wcs[0], other_end_wcs[0]),
            max(self_end_wcs[1], other_end_wcs[1])
        )
        new_wcs = self_wcs.deepcopy()
        new_wcs.crval = new_origin_wcs
        new_end_pix = [
            numpy.ceil(i+1) for i in
            new_wcs.all_world2pix(new_end_wcs[0], new_end_wcs[1], 0)
        ]

        new_data = numpy.ndarray(shape=new_end_pix)
        self_origin_in_new_data = new_wcs.all_world2pix(
            self_origin_wcs[0],
            self_origin_wcs[1],
            0
        )
        other_origin_in_new_data = new_wcs.all_world2pix(
            other_origin_wcs[0],
            other_origin_wcs[1],
            0
        )

        self.sum_pixels(self, new_data, self_origin_in_new_data)

        # Map other's pixels onto self's, summing values
        self.sum_pixels(other, new_data, other_origin_in_new_data)

        self.combined_data = new_data
        for k, v in new_wcs.to_header().items():
            if k in self.header:
                self.header[k] = v

        hdu_out = astropy.io.fits.PrimaryHDU(
            self.combined_data,
            self.header
        )
        self.hdu_list = astropy.io.fits.HDUList([hdu_out])

    def origin_for(self, other):
        other_wcs = astropy.wcs.WCS(other.hdu_list[0].header)
        self_wcs = astropy.wcs.WCS(self.hdu_list[0].header)

        other_origin = other_wcs.all_pix2world(0, 0, 0)

        return self_wcs.all_world2pix(
            other_origin[0],
            other_origin[1],
            0
        )

    """
    Sums data from source onto destination.

    Parameters:
        - source: source data array
        - destination: destination data array
        - start_coord: tuple. Starting coordinate to write in destination
    """
    def sum_pixels(self, source, destination, start_coord):
        # Need to check which way around these should be
        end_coord = (
            start_coord[0] + len(source.hdu_list[0].data[0]),
            start_coord[1] + len(source.hdu_list[0].data)
        )

        for out_x, source_row in zip(
            numpy.arange(start_coord[0], end_coord[0]),
            source.hdu_list[0].data
        ):
            for out_y, source_pixel in zip(
                numpy.arange(start_coord[1], end_coord[1]),
                source_row
            ):
                destination[out_x][out_y] += source_pixel
