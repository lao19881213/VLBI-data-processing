#Program to search the sources which have two wavebands of 
#contemporaneous observations in astrogeo website.

'''
How to run: 
Run the following command on the terminal:

export LC_ALL='en_US.utf8'
python3 search-SMBHBs.py

Inputs:
The 'redshift_sources.dat' file created using the program 'redshift-hist-sources.py'.

Outputs:
The "smbhb_condidates.dat" file having source name and the names of 
wavebands of observation along with observation date on Astrogeo website.
'''
import pandas as pd
import numpy as np
import sys
import os


#Estimating the starting time of this program:
import time
t0=time.time()

#Check the existence of input file:
if not os.path.isfile('redshift_sources.dat'):
    print("Input file 'redshift_sources.dat' does not exist.")
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

#Read the input data file:
df=pd.read_csv('redshift_sources.dat', sep=' ',na_filter=False,header=0)

#Replace a pattern with another pattern in a column:
import re
with open ("aa1", "w") as outfile:
    for line in df['Name']:
        modified = re.sub('[+]','%2B', line)
        outfile.writelines(modified)
        outfile.writelines('\n')

#Use the Astrogeo object names in the Astrogeo object search website to get 
#the information about observing waveband and epoch of observation for them: 
from bs4 import BeautifulSoup as bp
from urllib.request import urlopen as uReq

#Make function to estimate days between two dates:
from datetime import datetime
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y.%m.%d")
    d2 = datetime.strptime(d2, "%Y.%m.%d")
    return abs((d2 - d1).days)

infile = open('aa1', 'r')
outfile= open("aa2", "w")
i=0
for line in infile.readlines():
    my_url = 'http://astrogeo.org/cgi-bin/imdb_get_source.csh?source='+ line[0:(len(line)-1)]
    uClient=uReq(my_url)
    page_html=uClient.read()
    uClient.close()
    page_parse=bp(page_html,"html.parser")
    containers=page_parse.findAll("td",{"align":"RIGHT","nowrap":""})
    i=i+1
    out=open("kk.{}".format(i), "w")
    for x in range(6,len(containers),3):
        container=containers[x]
        out.write(container.text)
    out.close()
    #remove the blank lines for a text file:
    with open("kk.{}".format(i),'r') as inp:
        with open("ll.{}".format(i),'w') as out:
            for line1 in inp:
                if not line1.isspace():
                    out.write(line1)
    #Check for the nearly simultaneous and different bands observations:
    df=pd.read_csv("ll.{}".format(i), sep=' ',header=None,names=['Date','Band'])
    for j,k in zip(range(len(df)),range(1,len(df))):
        d1=df['Date'][j]
        d2=df['Date'][k]
        b1=df['Band'][j]
        b2=df['Band'][k]
        if days_between(d1,d2)<365 and b1 != b2:
            outfile.write(line)
outfile.close()
infile.close()

#Remove the duplicate lines from a text file:
uniquelines = set(open('aa2','r').readlines())
out=open('aa3', 'w').writelines(set(uniquelines))

#Replace a pattern with another pattern in a column:
with open ("aa3", "r") as infile:
    with open ("aa4", "w") as outfile:
        for line in infile:
            modified = re.sub('%2B','+', line)
            outfile.writelines(modified)

#Concate aa4 and redshift_sources.dat to make newsource_list.dat:
df1=pd.read_csv('aa4', sep=' ',header=None,names=['Name'])
df2=pd.read_csv('redshift_sources.dat', sep=' ',na_filter=False,header=0)
df3=pd.merge(df1, df2, how='left', on='Name')
df3.to_csv('smbhb_condidates.dat', sep=' ', header=['Name','RA','DEC','Redshift','Sep_arcmin'], index=False)

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

