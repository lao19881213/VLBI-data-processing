#Program to download fits image file of highest resolution 
#latest observation image from the astrogeo website.

'''
How to run: 
Run the following command on the terminal:

export LC_ALL='en_US.utf8'
python3 search-SMBHBs1.py

Inputs:
The 'smbhb_condidates.dat' file created using the program 'search-SMBHBs.py'.

Outputs:
The fits map files, one for each object in the input source list.
These image files have the highest resolution and latest available observation. 
'''
import pandas as pd
import numpy as np
import sys
import os


#Estimating the starting time of this program:
import time
t0=time.time()

#Check the existence of input file:
if not os.path.isfile('smbhb_condidates.dat'):
    print("Input file 'smbhb_condidates.dat' does not exist.")
    sys.exit(3)

#Check the Internet connection with timeout of 10 seconds:
import requests
def connected_to_internet(url='http://astrogeo.org/', timeout=10):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

if connected_to_internet()==False:
    sys.exit(3)


#Delete the temporary files if they already exist:
cwd = os.getcwd()
files=['aa','kk','ll']
for x in files:
    sub_f=[ f for f in os.listdir(cwd) if f.startswith(x) ]
    for f in sub_f:
        if os.path.isfile(f):
            os.remove(os.path.join(cwd, f))

#Delete the fits files if they already exist:
cwd = os.getcwd()
sub_f=[ f for f in os.listdir(cwd) if f.endswith('.fits') ]
for f in sub_f:
    if os.path.isfile(f):
        os.remove(os.path.join(cwd, f))

#Read the input data file:
df=pd.read_csv('smbhb_condidates.dat', sep=' ',na_filter=False,header=0)

#Replace a pattern with another pattern in a column:
import re
with open ("aa1", "w") as outfile:
    for line in df['Name']:
        modified = re.sub('[+]','%2B', line)
        outfile.writelines(modified)
        outfile.writelines('\n')

#Use the Astrogeo object names in the Astrogeo object search website to get 
#the name of image fits file of latest observation in the highest resolution band: 
from bs4 import BeautifulSoup as bp
from urllib.request import urlopen as uReq
#The available VLBA bands are: Q-band=43 GHz, K-band=22 GHz, U-band=15.3 GHz,
#X-band=8.4 GHz, C-band=5 GHz, S-band=2.3 GHz, L-band=1.4 GHz
pattern1 = re.compile(r'_Q_\s*')
pattern2 = re.compile(r'_K_\s*')
pattern3 = re.compile(r'_U_\s*')
pattern4 = re.compile(r'_X_\s*')
pattern5 = re.compile(r'_C_\s*')
pattern6 = re.compile(r'_S_\s*')
#
infile = open('aa1', 'r')
outfile= open("aa2", "w")
i=0
for line in infile.readlines():
    my_url = 'http://astrogeo.org/cgi-bin/imdb_get_source.csh?source='+ line[0:(len(line)-1)]
    uClient=uReq(my_url)
    page_html=uClient.read()
    uClient.close()
    page_parse=bp(page_html,"html.parser")
    containers=page_parse.findAll("td",{"align":"LEFT","nowrap":""})
    i=i+1
    out=open("kk.{}".format(i), "w")
    for x in range(4,len(containers),1):
        container=containers[x].tt
        sub_containers=container.findAll("a")
        for y in range(2,len(sub_containers),4):
            sub_container=sub_containers[y]['href']
            out.write(sub_container)
            out.write('\n')
    out.close()
    #To print the lines having a pattern in a file into another file:
    inp = open("kk.{}".format(i), 'r')
    out=open("ll.{}".format(i), 'w')
    for line in inp:
        if pattern1.search(line):
            out.write(line)
    out.close()
    if os.stat("ll.{}".format(i)).st_size==0:
        inp = open("kk.{}".format(i), 'r')
        out=open("ll.{}".format(i), 'w')
        for line in inp:
            if pattern2.search(line):
                out.write(line)
        out.close()
    if os.stat("ll.{}".format(i)).st_size==0:
        inp = open("kk.{}".format(i), 'r')
        out=open("ll.{}".format(i), 'w')
        for line in inp:
            if pattern3.search(line):
                out.write(line)
        out.close()
    if os.stat("ll.{}".format(i)).st_size==0:
        inp = open("kk.{}".format(i), 'r')
        out=open("ll.{}".format(i), 'w')
        for line in inp:
            if pattern4.search(line):
                out.write(line)
        out.close()
    if os.stat("ll.{}".format(i)).st_size==0:
        inp = open("kk.{}".format(i), 'r')
        out=open("ll.{}".format(i), 'w')
        for line in inp:
            if pattern5.search(line):
                out.write(line)
        out.close()
    if os.stat("ll.{}".format(i)).st_size==0:
        inp = open("kk.{}".format(i), 'r')
        out=open("ll.{}".format(i), 'w')
        for line in inp:
            if pattern6.search(line):
                out.write(line)
        out.close()
    #Write the last line of a file to another file:
    lines = open("ll.{}".format(i), 'r').readlines()
    outfile.writelines(lines[-1:])
outfile.close()
infile.close()


#Download the fits image files:
import urllib.request
infile = open('aa2', 'r')
outfile= open("aa3", "w")
for line in infile.readlines():
    my_url = 'http://astrogeo.org/'+ line[0:(len(line)-1)]
    #print(my_url)
    file_name = my_url.split('/')[-1]
    print(file_name,file=outfile)
    urllib.request.urlretrieve (my_url,file_name)
outfile.close()
infile.close()

#Delete the temporary files:
cwd = os.getcwd()
files=['aa','kk','ll']
for x in files:
    sub_f=[ f for f in os.listdir(cwd) if f.startswith(x) ]
    for f in sub_f:
        if os.path.isfile(f):
            os.remove(os.path.join(cwd, f))

#Estimating the ending time of this program:
t1=time.time()
print('Time taken by the program:', np.round(t1-t0,2), 'seconds')

