import astropy.io.fits as fits
import matplotlib.pyplot as plt
import numpy as np
import os
import sep
from matplotlib.patches import Ellipse
import xlwt
from astropy.table import Table
from mpl_toolkits.axes_grid1 import make_axes_locatable

def pltim(d):
    plt.imshow(d,origin='lower')
    plt.colorbar()
    plt.title(souname)
    plt.show()

def fitsmask(souname):
    pbdata = fits.getdata(maindir+souname+'/'+souname+'.cont.pb.fits')
    pbmask = pbdata > 0.5
    mask=fits.getdata(maindir+souname+'/'+souname+'.cont.image.pbcor.fits')
    mask_1=np.isfinite(mask)*(mask>0.0)*(1-np.isnan(mask))
    mask_2=mask*mask_1
    mask_3=(1-pbmask)
    mask_4=mask_3>0.5
    return(mask_4,mask_2)

def sepfits(souname):
    center,mask=fitsmask(souname)
    bkg=sep.Background(mask)
    print('background: '+str(bkg.globalback)+'    rms: '+str(bkg.globalrms))
    # pltim(bkg.back())
    # pltim(bkg.rms())
    data=np.nan_to_num(mask-bkg)
    pltim(data)
    obg,re=sep.extract(data, thresh=0.015,minarea=10,deblend_cont=0.0001,deblend_nthresh=128,segmentation_map=True,mask=center)
    # obg,re=sep.extract(data, 3, err=bkg.globalrms,minarea=10,deblend_cont=0.0001,deblend_nthresh=128,segmentation_map=True,mask=center)
    print(str(len(obg))+'core(s)')
    for i in range(len(obg)):
        x,y,f=obg['x'][i],obg['y'][i],obg['flux'][i]
        print('x,y='+str(x)+'   '+str(y)+'        flux='+str(f))
    pltim(re)
    fig, ax = plt.subplots()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    im = ax.imshow(data, interpolation='nearest',origin='lower')
    plt.title(souname+'_show_regions')
    fig.colorbar(im, cax=cax, orientation='vertical')
    for i in range(len(obg)):
        e = Ellipse(xy=(obg['x'][i], obg['y'][i]),
                    width=4*obg['a'][i],
                    height=4*obg['b'][i],
                    angle=obg['theta'][i] * 180. / np.pi)
        e.set_facecolor('none')
        e.set_edgecolor('red')
        ax.add_artist(e)
    # plt.savefig(souname+'.png',dpi=300)
    # plt.savefig('SEP-test-DR1/'+souname+'.pdf')plt.title(souname+'_show_regions')
    plt.show()
    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet('Datasheet')
    types=['number','thresh','npix','tnpix','xmin','xmax','ymin','ymax',
        'x','y','x2','y2','xy','errx2','erry2','errxy','a','b','theta','cxx','cyy','cxy',
        'cflux','flux','cpeak','peak','xcpeak','ycpeak','xpeak','ypeak']
    for i in range(len(types)):
        worksheet.write(0,i, label = types[i])
    ista=1
    for i in range(len(obg)):
        worksheet.write(ista,0, label = i+1)
        for j in range(len(types)-1):
            worksheet.write(ista,j+1, label =str(obg[types[j+1]][i]))
        ista+=1    
    workbook.save('SEP-test-DR1/'+souname+'_%2e_%2e.xls'%(bkg.globalback, bkg.globalrms))
    return(obg)

maindir = './'
soulist = Table.read('testsample.txt', format='ascii.no_header')
for i in range(len(soulist)):
    souname = soulist['col1'][i]
    re=sepfits(souname)
# souname='I09094-4803'
# re=sepfits(souname)

