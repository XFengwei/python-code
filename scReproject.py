######################################################################
# JCMT usually offers data with a rotation of specific angle, relative
# to world coordinates (Ra. & Dec.)
######################################################################

from astropy import units as u
import numpy as np
from astropy import wcs
from spectral_cube import SpectralCube as sc
from reproject import reproject_interp

input = ''
sc.read(,hdu=0)


