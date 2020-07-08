import numpy as np
import os.path
import math
import sys

from read_netcdf_2D import read_netcdf_2D

###   read in data and make composite average - full  values (not anomaly !!) 
def get_flux_clima(imax, jmax, im1, im2, variable,  dataout, prefixclim, undef):

    itmax = 12
    ss    = np.ma.zeros((imax,jmax),dtype='float32', order='F')      
    vvar  = np.ma.zeros((imax,jmax, itmax),dtype='float32', order='F')
    dataout = np.ma.zeros((imax,jmax),dtype='float32', order='F')
##  read x, y, t dimensioned data 
    namein = prefixclim + variable + ".grd"

    if (os.path.exists( namein)):
        vvar = read_netcdf_2D(imax, jmax, itmax,  variable,  namein, vvar, undef)
        vvar_invalid = (vvar >= undef)
        for im in range (im1, im2+1):
                     imm = im
                     if( im > 12 ):
                            imm = im - 12
                            dataout[:,:] += vvar[:,:, imm-1]
                            ss[~vvar_invalid, imm-1] += 1.

    else:
        print " missing file " +  namein
        print " exiting get_flux_clima.py "
        sys.exit()

###  
    dataout = dataout/ss

    return dataout.filled(fill_value = undef)

