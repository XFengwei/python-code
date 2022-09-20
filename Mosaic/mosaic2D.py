# include packages
# pip install MontagePy==1.2.3
from MontagePy.main import mGetHdr, mHdr, mImgtbl, mMakeHdr, mProjectQL, mAdd
import os
import shutil
import glob

def mkdir(filePath):
    '''
    Delete the original file first and then initate a new one
    '''
    try:
        shutil.rmtree(filePath)
    except:
        pass
    os.mkdir(filePath)

def make_mosaic(pre_mosaic_path='./', proj_path = './proj/', final_path = './final/', output_name = 'final_mosaic.fits'):
    '''
    
    '''
    rtn =  mImgtbl(pre_mosaic_path, 'pre_mosaic.tbl') # create pre-mosaic image list
    print("mImgtbl (pre-mosaic image table):  " + str(rtn), flush=True) # update the process
    mMakeHdr('pre_mosaic.tbl', 'mosaic_template.hdr') # create the header for the mosaic
    mkdir(proj_path)
    for each in glob.glob('*.fits'):
        # reproject all the pre-mosaic fields into the same template header
        mProjectQL(each, proj_path + each[:-5] + '_proj.fits',pre_mosaic_path + 'mosaic_template.hdr')
    rtn = mImgtbl(proj_path, 'reprojected.tbl')
    print("mImgtbl (reprojected image table):  " + str(rtn), flush=True) # update the process
    mkdir(final_path)
    rtn = mAdd('./', 'reprojected.tbl', 'mosaic_template.hdr', final_path+'final_mosaic.fits',debug=1)
    print("mAdd:  " + str(rtn), flush=True)
