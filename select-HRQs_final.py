# Program to select quasars from astrogeo website.

'''
How to run: 
Run the following command on the terminal:

export LC_ALL='en_US.utf8'
python3 select-HRQs.py


Inputs:
No input required.

Outputs:
"source_list.dat" file having source name on Astrogeo website,
its RA & DEC cooredinates from Asytrogeo website, and its 
redshift from NED website.
'''

import numpy as np
import sys
import os
import logging

logger = logging.getLogger('select-HRQs')
logfile = "./select_HRQs.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG)

#Estimating the starting time of this program:
import time
t0=time.time()

#First Check the Internet connection with timeout of 5 seconds:
import requests
def connected_to_internet(url='http://astrogeo.org/', timeout=15):
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
files=['aa','bb','cc','kk','ll','mm','nn']
for x in files:
    sub_f=[ f for f in os.listdir(cwd) if f.startswith(x) ]
    for f in sub_f:
        if os.path.isfile(f):
            os.remove(os.path.join(cwd, f))


###########################################################################
# First Step: Select the list of sources from Astrogeo website            #
###########################################################################

from bs4 import BeautifulSoup as bp
from urllib.request import urlopen as uReq

#Make the website url as a variable:
my_url='http://astrogeo.org/cgi-bin/imdb_get_source.csh'

#Open the url:
uClient=uReq(my_url)

#Read the url and save its content as a variable:
page_html=uClient.read()

#Close the url:
uClient.close()

#Parse (i.e analyze) the html page into its parts:
page_parse=bp(page_html,"html.parser")

#See the parts of the html page within the variable 'page_parse' in 
#a structured way (or organized format) so that the sub-parts of this 
#variable having the required informations can be identified:
#print(bp.prettify(page_parse))

#find the sections or parts of the parsed html page which has 
#all the required information and save it as a variable:
containers=page_parse.findAll("table",{"cellpadding":"3%"})

#Check the length of the variable 'containers' to know the 
#number of sections of the same type has the required information.
#print(len(containers))

#Select the first section within container and save it as a variable:
container=containers[0]

#Now see the parts of the html page within the variable 'container' to 
#identify the sub-parts of this variable having the required informations:
#print(bp.prettify(container))

#We see that our needed informations are within this variable 'container'.
#Otherwise we have to again run the findAll() function as follows:
#sub_container=container.findAll("html_tag_name",{"attribute":"attribute_value"})
#And then proceed as given above.

#Print all the text information within container:
#print(container.text)

#Write the text stored within container variable to a text file:
with open("aa.1", "w") as text_file:
    text_file.write(container.text)  


'''
#Remove all blank lines:
with open('aa.1') as in_file, open('aa.1', 'r+') as out_file:
    out_file.writelines(line for line in in_file if line.strip())
    out_file.truncate()

#Remove the 11 lines from top and 3 lines from bottom:
lines = open('aa.1').readlines()
open('aa.2', 'w').writelines(lines[11:-3])
'''

#Remove every alternate lines from a file:
with open("aa.2","w") as output: 
    lines = open( 'aa.1', "r" ).readlines()
    output.writelines(lines[2::2])
    
#Copy selected column from the ascii file and save into a file:
f = open('aa.2', 'r')
with open("aa.3", "w") as text_file:
    #print("#List of sources from astrogeo.org image database", file=text_file)
    for line in f:
        line = line.strip()
        columns = line.split()
        name = columns[0]
        print(name, file=text_file)
f.close()

#Copy selected lines from a file and save into a file:
with open("aa.4","w") as output: 
    lines = open( 'aa.3', "r" ).readlines()
    output.writelines(lines[:])

#Print the total number of sources and number source for which program is running:
lines1 = open('aa.3').readlines()
logging.info('Total number of sources:%d' % len(lines1))
lines2 = open('aa.4').readlines()
if len(lines1)==len(lines2):
    logging.info('Program is running for all sources.')
else:
    logging.info('Program is running for %d sources.' % len(lines2))


#############################################################################################
# Second Step: Select the RA & DEC coordinates of the source list from Astrogeo website     #
#############################################################################################

#Replace '+' with '%2B' pattern in the text file:
import re
with open ("aa.4", "r") as infile:
    with open ("bb.1", "w") as outfile:
        for line in infile:
            modified = re.sub('[+]','%2B', line)
            outfile.writelines(modified)

'''#or use this one:
infile = open('aa.3', 'r')
outfile = open('bb.1', 'w')
for line in infile:
    modified = re.sub('[+]','%2B', line)
    outfile.write(modified)
 
infile.close()
outfile.close()
'''

#Use the Astrogeo object names in the Astrogeo object search website to get 
#their RA & DEC coordinates and save them in separate files: 
infile = open('bb.1', 'r')
#outfile1= open("bb.2", "w")
#outfile2= open("bb.3", "w")
import multiprocessing as mp
def process_wrapper(lineID):
    outfile1= open("bb.2", "a+")
    outfile2= open("bb.3", "a+")
    with open("bb.1") as infile:
         for i,line in enumerate(infile):
             if i != lineID:
                continue
             else:
                line = infile.readline()
                my_url = 'http://astrogeo.org/cgi-bin/imdb_get_source.csh?source='+ line[0:(len(line)-1)]
                #print(lineID)
                uClient=uReq(my_url)
                page_html=uClient.read()
                uClient.close()
                page_parse=bp(page_html,"html.parser")
                containers=page_parse.findAll('tr', {"valign":"TOP"})
                if len(containers)!=0:
                   container=containers[0]
                   sub_containers=container.findAll("td", {'align':'RIGHT'})
                   sub_container1=sub_containers[1]
                   sub_container2=sub_containers[2]
                   print(sub_container1.text, file=outfile1)
                   print(sub_container2.text, file=outfile2)
                else:
                   print('11:11:11.1111', file=outfile1)
                   print('+11:11:11.111', file=outfile2)
                   logging.info('Source not found in the Astrogeo catalogue: %s' % line)
    outfile1.close()
    outfile2.close()

#init objects
pool = mp.Pool(40)
jobs = []
#create jobs
with open("bb.1") as f:
     for ID,line in enumerate(f):
         jobs.append(pool.apply_async(process_wrapper,(ID,)))

#wait for all jobs to finish
for job in jobs:
    job.get()

#clean up
pool.close()

#Change the RA & DEC format to read from NED:
f = open('bb.2', 'r')
with open("bb.4", "w") as text_file:
    for line in f:
        line = line.strip()
        columns = line.split(':')
        print(columns[0],'h',columns[1],'m',columns[2],'s', file=text_file)
f.close()

f = open('bb.3', 'r')
with open("bb.5", "w") as text_file:
    for line in f:
        line = line.strip()
        columns = line.split(':')
        print(columns[0],'d',columns[1],'m',columns[2],'s', file=text_file)
f.close()

with open ("bb.4", "r") as infile:
    with open ("bb.6", "w") as outfile:
        for line in infile:
            modified = re.sub(' ','', line)
            outfile.writelines(modified)

with open ("bb.5", "r") as infile:
    with open ("bb.7", "w") as outfile:
        for line in infile:
            modified = re.sub(' ','', line)
            outfile.writelines(modified)


#####################################################################################################
# Third Step: Use the RA & DEC coordinates to get the redshift of the source list from NED website  #
#####################################################################################################

#Search the sources within 6 arcseconds around the obtained coordinates
#in previous step using NED website and take the redshift of the expected 
#radio source:
#z_out=open("cc.1", "w")
#i=0
def process_third_step(lineID):
    z_out=open("cc.1", "a+")
    with open('bb.6', 'r') as f1, open('bb.7', 'r') as f2:
         for ID, line in enumerate(zip(f1, f2)):
                if ID != lineID:
                   continue
                else:
                   x = line[0]
                   y = line[1]
                   my_url = 'http://ned.ipac.caltech.edu/cgi-bin/nph-objsearch?in_csys=Equatorial&in_equinox=J2000.0&lon='+ x[0:(len(x)-1)]+'&lat='+ y[0:(len(y)-1)]+'&radius=0.1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=Distance+to+search+center&of=pre_text&zv_breaker=30000.0&list_limit=32&img_stamp=YES&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z&ot_include=ANY&in_objtypes3=Radio&nmp_op=ANY&search_type=Near+Position+Search'
                   #print(my_url)
                   uClient=uReq(my_url)
                   page_html=uClient.read()
                   uClient.close()
                   page_parse=bp(page_html,"html.parser")
                   containers=page_parse.findAll('td', {"bgcolor":"lightgrey"})
                   if len(containers)!=0:
                      container=containers[0]
                   else:
                      my_url1 = 'http://ned.ipac.caltech.edu/cgi-bin/nph-objsearch?in_csys=Equatorial&in_equinox=J2000.0&lon='+ x[0:(len(x)-1)]+'&lat='+ y[0:(len(y)-1)]+'&radius=0.5&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=Distance+to+search+center&of=pre_text&zv_breaker=30000.0&list_limit=32&img_stamp=YES&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z&ot_include=ANY&in_objtypes3=Radio&nmp_op=ANY&search_type=Near+Position+Search'
                      uClient1=uReq(my_url1)
                      page_html1=uClient1.read()
                      uClient1.close()
                      page_parse1=bp(page_html1,"html.parser")
                      containers1=page_parse1.findAll('td', {"bgcolor":"lightgrey"})
                      if len(containers1)!=0:
                         container=containers1[0]
                      else:
                         my_url2 = 'http://ned.ipac.caltech.edu/cgi-bin/nph-objsearch?in_csys=Equatorial&in_equinox=J2000.0&lon='+ x[0:(len(x)-1)]+'&lat='+ y[0:(len(y)-1)]+'&radius=2.0&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=Distance+to+search+center&of=pre_text&zv_breaker=30000.0&list_limit=32&img_stamp=YES&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z&ot_include=ANY&in_objtypes3=Radio&nmp_op=ANY&search_type=Near+Position+Search'
                         uClient2=uReq(my_url2)
                         page_html2=uClient2.read()
                         uClient2.close()
                         page_parse2=bp(page_html2,"html.parser")
                         containers2=page_parse2.findAll('td', {"bgcolor":"lightgrey"})
                         if len(containers2)!=0:
                            container=containers2[0]
                         else:
                           my_url3 = 'http://ned.ipac.caltech.edu/cgi-bin/nph-objsearch?in_csys=Equatorial&in_equinox=J2000.0&lon=11h11m11.1111&lat=+11d11m11.111&radius=2.0&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=Distance+to+search+center&of=pre_text&zv_breaker=30000.0&list_limit=32&img_stamp=YES&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z&ot_include=ANY&in_objtypes3=Radio&nmp_op=ANY&search_type=Near+Position+Search'
                           uClient3=uReq(my_url3)
                           page_html3=uClient3.read()
                           uClient3.close()
                           page_parse3=bp(page_html3,"html.parser")
                           containers3=page_parse3.findAll('td', {"bgcolor":"lightgrey"})
                           container=containers3[0]
                           logging.info('Radio source not found within 2.0 arcmin radius from NED around coordinates:\n%s %s' % (x,y))
                   #i=i+1
                   outfile=open("kk.{}".format(ID), "w")
                   outfile.write(container.pre.text)
                   outfile.close()
                   #Removing the first 3 lines of a text file:
                   lines=open("kk.{}".format(ID), "r").readlines()
                   open("ll.{}".format(ID), 'w').writelines(lines[3:])
                   #Selecting particular columns based on their positions in a text file table:
                   inp = open("ll.{}".format(ID), 'r')
                   lines = inp.readlines()
                   out=open("mm.{}".format(ID), 'w')
                   for line in lines:
                       out.write(line[74:83])
                       out.write(line[120:123])
                       out.write("\n")
                   out.close()
                   inp.close()
                   #Sorting a text file table with respect to a column of numbers:
                   with open("mm.{}".format(ID), 'r') as inp:
                        with open("nn.{}".format(ID), 'w') as out:
                             lines = inp.readlines()
                             lines.sort(key=lambda line: int(line.split()[1]), reverse=True)
                             out.writelines(lines)
                   #Selecting a particular element of text file table:
                   inp = open("nn.{}".format(ID), 'r').readlines()
                   line = inp[0].split() 
                   if line[0]=='...':
                      z_value='NaN'    #We can make it '0.0' also.
                   else:
                      z_value=line[0]
                   z_out.write(z_value)
                   z_out.write('\n')
    z_out.close()

#init objects, use 68 processes
pool = mp.Pool(40)
jobs = []
#create jobs
with open("bb.6") as f:
     for ID,line in enumerate(f):
         jobs.append(pool.apply_async(process_third_step,(ID,)))

#wait for all jobs to finish
for job in jobs:
    job.get()

#clean up
pool.close()

##Writing and executing a program inside a python program:
#f= open("cc1.py","w")
#lines=r'''#!/home/sumit/Optical/anaconda3/bin/python
#
#import re;import os
#with open ('cc.1', 'r') as infile:
#    with open ("cc.2", "w") as outfile:
#        for line in infile:
#            outfile.writelines(line)
#'''
#f.write(lines)
#f.close()
##This program can be run as:
#os.system('python cc1.py')
##or as:
#import cc1


###########################################################################
# Forth Step: Join all the required information in a final source table   #
###########################################################################

#To write many files in a file column-wise:
import pandas as pd
files=['aa.4','bb.6','bb.7','cc.1']
frames = [ pd.read_csv(x, sep=' ',na_filter=False, header=None) for x in files ]
df = pd.concat(frames,axis=1)
df.to_csv('source_list.dat', sep='\t', header=['Name','    RA','             DEC','        Redshift'], index=False)


#Delete the temporary files if they already exist:
cwd = os.getcwd()
files=['aa','bb','cc','kk','ll','mm','nn']
for x in files:
    sub_f=[ f for f in os.listdir(cwd) if f.startswith(x) ]
    for f in sub_f:
        if os.path.isfile(f):
            os.remove(os.path.join(cwd, f))


#Estimating the ending time of this program:
t1=time.time()
run_time = np.round(t1-t0,2)
logging.info('Time taken by the program: %f seconds' % run_time)

