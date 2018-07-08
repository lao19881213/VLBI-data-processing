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


difmap = pexpect.spawn('difmap')
difmap.expect('0>')
p = re.compile(r'(difmap.log_?\d*)')
logfile = p.findall(difmap.before.decode())[0]
