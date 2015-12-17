import astropy
#import bottleneck as bn
import ccdproc
import numpy as np
import os
import progressbar as pb
import reproject as reproj
import sys

# Based in part on http://nbviewer.ipython.org/gist/mwcraig/06060d789cc298bbb08e

pbwidgets = lambda s: [" %s: " % (s,), pb.Percentage(), ' ', pb.Bar(marker='='),
                       ' ', pb.ETA()]
mkprogress = lambda s, n: pb.ProgressBar(widgets=pbwidgets(s), maxval=n).start()

def fits_in_dir(path):
    return [
        '%s/%s' % (path, f) for f in os.listdir(path) if (
            f.endswith('.fits') or f.endswith(".fz")
        ) and not f.startswith('_')
    ]

def load_files(file_names, reproject=False):
    if not reproject:
        fs = [
            ccdproc.CCDData.read(file_name) for file_name in file_names
        ]
        file_count = len(fs)
    else:
        hdu_lists = [
            astropy.io.fits.open(file_name) for file_name in file_names
        ]

        file_count = len(hdu_lists)

       # progress = mkprogress("Reprojecting images", file_count)

        fs = []
        for i, h in enumerate(hdu_lists):
            try:
                rpd = reproj.reproject_interp(h, h[1].header, hdu_in=1)[0]
            except:
                print file_names[i]
                raise

            fs.append(ccdproc.CCDData(
                rpd,
                unit="adu"))
        #    progress.update(i)

    return (fs, file_count)

# TODO: See if this is actually needed, or if there's something built into numpy now
def bn_median(masked_array, axis=None):
    """
    Perform fast median on masked array

    Parameters
    ----------

    masked_array : `numpy.ma.masked_array`
        Array of which to find the median.

    axis : int, optional
        Axis along which to perform the median. Default is to find the median of
        the flattened array.
    """
    data = masked_array.filled(fill_value=np.NaN)
    med = bn.nanmedian(data, axis=axis)
    # construct a masked array result, setting the mask from any NaN entries
    return np.ma.array(med, mask=np.isnan(med))


gain = 2.87 * astropy.units.electron / astropy.units.adu
readnoise = 2.1 * astropy.units.electron

#bias_data = load_files(fits_in_dir('bias'))
#bias_combiner = ccdproc.Combiner(bias_data)
#combined_bias = bias_combiner.average_combine()

# TODO: Sigma clipping?
#print "Combining flat fields..."
#flat_data, flat_file_count = load_files(fits_in_dir('flats'))
#flat_combiner = ccdproc.Combiner(flat_data)
#flat_combiner.sigma_clipping()
#
#flat_combiner.scaling = lambda arr: 1/np.ma.average(arr)
#
#combined_flat = flat_combiner.median_combine(median_func=bn_median)
# TODO: Each image has header['GAIN'] -- check if they're different
#combined_flat = ccdproc.gain_correct(combined_flat, gain=gain)


image_data, image_file_count = load_files(fits_in_dir('o20130513T204839'),
                                          reproject=True)
#_image_data = []
#progress = mkprogress("Flat field correction", image_file_count)
#for i, image in enumerate(image_data):
#    _image_data.append(
#        ccdproc.flat_correct(ccdproc.gain_correct(image, gain=gain),
#                             combined_flat))
#    progress.update(i)
#image_data = _image_data

print "\nCombining images..."
images_combiner = ccdproc.Combiner(image_data)
combined_images = images_combiner.average_combine()

print "Writing output to %s" % (sys.argv[1],)
combined_images.write(sys.argv[1])
