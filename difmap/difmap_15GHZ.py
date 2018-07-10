# -*- coding: utf-8 -*-
"""
Created on 08-07-2018

@author: lbq
"""
import numpy as np
import pexpect
import os
import re
from astropy.io.fits import getheader
import argparse

def difmap_process(uv_fits_file):
    difmap = pexpect.spawn('difmap')
    difmap.expect('0>')
    p = re.compile(r'(difmap.log_?\d*)')
    logfile = p.findall(difmap.before.decode())[0]
    #Read data
    difmap.sendline('obs %s' % uv_fits_file)
    difmap.expect('0>')
    #Select polarization
    difmap.sendline('select i')
    difmap.expect('0>')
    #uv plot
    difmap.sendline('uvplot')
    #difmap.expect('0>')
    difmap.sendline(r'device uv.ps/vps')
    difmap.expect('0>')
    #mapsize 
    difmap.sendline('mapsize 512')
    difmap.expect('0>')
    #mapplot
    difmap.sendline('mapl')
    difmap.expect('0>')
    difmap.sendline(r'device tmp.ps/vps')
    difmap.expect('0>')
    #clean
    difmap.sendline('clean 300, 0.05; mapl; selfcal; mapl;')
    difmap.expect('0>')
    difmap.sendline(r'device tmp.ps/vps')
    difmap.expect('0>')
    difmap.sendline('clean 300, 0.05; mapl')
    difmap.expect('0>')
    difmap.sendline(r'device tmp.ps/vps')
    difmap.expect('0>')
    difmap.sendline('clean 300, 0.05; mapl')
    difmap.expect('0>')
    difmap.sendline(r'device tmp.ps/vps')
    difmap.expect('0>')
    #uvweight
    difmap.sendline('uvwei 0,-1;mapl')
    difmap.expect('0>')
    difmap.sendline(r'device tmp.ps/vps')
    difmap.expect('0>')
    #clean
    difmap.sendline('clean 300, 0.05; mapl')
    difmap.expect('0>')
    difmap.sendline(r'device tmp1.ps/vps')
    difmap.expect('0>',timeout=3600)

    #exit difmap
    #difmap.expect('0>')
    difmap.sendline('quit')
    difmap.close()

if __name__ == "__main__":
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Difmap data processing')
    
    parser.add_argument('--uvfitsfile', dest='uv_fits_file', help='uv fits file input',
                        default='', type=str)


    args = parser.parse_args()
   
    difmap_process(args.uv_fits_file) 
