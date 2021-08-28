## Python Scripts For Astronomical Data (FITS) Reprojection

Obviously, the development of astronomy and astrophysics is strongly based on the the update of instruments/telescopes. Before the globalization of astronomy, astronomers/engenieers have been building telescopes on behalf of their own countries or even institutions, so it's not strange that each telescope produces its own data as well as the unique application to reduce the data. Nowadays, faced with the multi-wavelength data, we find it so easy to lose ourselves once we have to deal with data from more than one telescopes. In the past decade years, our astronomers have been struggling for a unified data format and a corresponding data-reducing application. And that's the reason why **Flexible Image Transport System (FITS)** came to birth.

After the popularity of FITS files, many tools help convert different data format to FITS. Python, a very open language also join, as a emerging force. Nowadays, people find it convenient to install and use open Python packages, just like what we are doing here. **However**, FITS files don't always fit you. As a flexible data format, it permit colorful parameters to translate the data. In other words, if you ever touch FITS file, one DATA have infinite possiblities based on your HEADER. What we are trying to do here is to make things easier, to help you translate the data cube into universal one, which strongly help you to apply your existing codes for further analyses.

Updated on 8.27, 2021
Fengwei Xu

## Tutorial
Download all the files but **BG081_HCN(4-3).cut20.fits** and **Astroreproject.py** are important.

You need Python3 installed and the basic packages are needed:
1. Numpy ==> 1.19.5
2. Astropy ==> 4.0.1
3. spectral-cube ==> 0.4.5
4. reproject ==> 0.7.1

After running
```terminal
Python3 Astroreproject.py
```
in your terminal, you could get product **HCN(4-3)_cube_rp.fits** and **HCN(4-3)_MomZer_rp.fits**
