

import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

from db_module import push_data

import urllib2
from bs4 import BeautifulSoup
import cookielib
import re
import itertools
import os

import re
import csv

import itertools




def Gov_Ltgov():

	try:
	    	
	    
	    	
	    opener = urllib2.build_opener()
	    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	    response = opener.open('http://nj.gov/governor/')
	    html_contents = response.read()
	    # print html_contents
	    soup = BeautifulSoup( html_contents,"html.parser" )
	    # print soup.find("div", {'id': 'secondary_col2'})
	    data = []
	    
	    d= (soup.find("div", {'class': 'gov-bar pull-right'}).get_text('|',strip=True).encode("ascii",'ignore')).split('|') 

	    data.append(['New Jersey',d[0].split(' ',1)[1],d[0].split(' ',1)[0]])
	    data.append(['New Jersey',d[2].split(' ',2)[2],' '.join(d[2].split(' ',2)[:2]),])
	    print data
	        # data.append([d[1],d[5],d[0],d[2],d[4]])
	    # print data
	    data=[[(j.strip()).capitalize() for j in i] for i in data]
	    with open('State\\Gov_Ltgov.csv','wb') as out:
	        csv_out=csv.writer(out)
	        csv_out.writerow(["State","Name","Designation"])
	        for row in data:
	            csv_out.writerow(row)



	    with open('State\\Gov_Ltgov.csv','rb') as out:
	        dddd = []
	        data=csv.DictReader(out)
	        # print data
	        for i in data:
	            dddd.append(i)
	        # print d
	        push_data.for_gov_lt(dddd)
	        print "pushed"
	except Exception, e:
		logger.error('GOVERNER AND LT giverner ,state, Description:'+str(e))