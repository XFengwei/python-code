######################################################################
# JCMT usually offers data with a rotation of specific angle, relative
# to world coordinates (Ra. & Dec.) system. This Python script help to
# reproject the data (2d/3d) into regular system. Practically, it just
# rotate the data for you.
# Updated on 2021.8.27 by Fengwei
######################################################################

from astropy import units as u
import numpy as np
from astropy.io import fits
from astropy import wcs
from spectral_cube import SpectralCube as sc
from reproject import reproject_interp

input = './BG081_HCN(4-3).cut20.fits' # input data to be reprojected
hcn = sc.read(input,hdu=0) # JCMT HARPS HCN(4-3) data cube
w0 = wcs.WCS(hcn.header)

hcn_m0 = hcn.moment(order=0) # produce momzero map, a 2-D data
hdr = hcn_m0.hdu.header # get a 2-D header
w1 = wcs.WCS(hcn_m0.hdu.header)
hcn_m0 = np.nan_to_num(hcn_m0.hdu.data).astype(float) # nan to zero
hcn_m0_hdu = fits.ImageHDU(data = hcn_m0, header = w1.to_header())

newhdr = fits.Header()
newhdr['SIMPLE'] = (True, 'conforms to FITS standard')
newhdr['BITPIX'] = (-64, 'array data type')
newhdr['NAXIS'] = 2
cosphi = abs(hdr['PC1_1'])
sinphi = abs(hdr['PC1_2'])
oldpix = hdr['NAXIS1']
newpix = oldpix * (cosphi + sinphi) / np.sqrt(cosphi**2 + sinphi**2)
delta = np.sqrt(cosphi**2 + sinphi**2)
newhdr['NAXIS1'] = int(newpix) + 1
newhdr['NAXIS2'] = int(newpix) + 1
newhdr['CRPIX1'] = (int(newpix) + 1)/2
newhdr['CRPIX2'] = (int(newpix) + 1)/2
newhdr['CDELT1'] = -delta
newhdr['CDELT2'] = delta
newhdr['CUNIT1'] = ('deg','Units of coordinate increment and value')
newhdr['CUNIT2'] = 'deg'
newhdr['CTYPE1'] = 'RA---TAN'
newhdr['CTYPE2'] = 'DEC--TAN'

# find the coordinate of the center point
ORPIX1 = hdr['CRPIX1']
ORPIX2 = hdr['CRPIX2']
newhdr['CRVAL1'] = hdr['CRVAL1'] + (-delta)  * (oldpix/2+0.5-hdr['CRPIX1'])
newhdr['CRVAL2'] = hdr['CRVAL2'] + delta  * (oldpix/2+0.5-hdr['CRPIX2'])
newhdr['TELESCOP'] = ('JCMT', 'Name of Telescope')
newhdr['RADESYS'] = ('FK5','Equatorial coordinate system')
newhdr['EQUINOX'] = 2000.0
newhdr['BUNIT'] = 'K km/s'

hcn_m0_rp, footprint = reproject_interp(hcn_m0_hdu, newhdr)
# print(newhdr)
hcnm0_rp_hdu = fits.PrimaryHDU(hcn_m0_rp)
hcnm0_rp_hdu.header = newhdr
hcnm0_rp_hdu.writeto('HCN(4-3)_MomZero_rp.fits', overwrite=True)

w2 = wcs.WCS(hcn.header)
newhdr['NAXIS'] = 3
w3 = wcs.WCS(newhdr, naxis=3)
w3._naxis = [0,0,0]
w3.wcs.ctype = ['RA---TAN',  'DEC--TAN',  'VRAD' ]
w3.wcs.crval = [newhdr['CRVAL1'], newhdr['CRVAL2'], w2.wcs.crval[2]]
w3.wcs.crpix = [newhdr['CRPIX1'], newhdr['CRPIX2'], w2.wcs.crpix[2]]
w3.wcs.cdelt = [newhdr['CDELT1'], newhdr['CDELT2'], w2.wcs.pc[2,2]]
w3.wcs.pc = np.identity(3)

nx = newhdr['NAXIS1']
ny = newhdr['NAXIS2']
nv = len(hcn.spectral_axis)
_data, _fp = reproject_interp(hcn.hdu, output_projection=w3, shape_out=(nv,ny,nx))
hcn_rp = sc(data=_data,wcs=w3).with_spectral_unit(u.km/u.s)
hcn_rp.write('HCN(4-3)_cube_rp.fits',overwrite=True)
