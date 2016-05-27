from reducer.align import Aligner
from reducer.fits import FitsWrapper

# Takes two FITS images and stacks them (summing their pixel values)
class Stacker(FitsWrapper):
    aligner = None

    def __init__(self, in_file=None):
        super(Stacker, self).__init__(in_file)
        self.aligner = Aligner(self)

    def stack(self, other):
        self.aligner.align(other)
