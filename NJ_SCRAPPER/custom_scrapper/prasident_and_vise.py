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




def prasident_and_vise():
    try:


   
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open('https://vote-usa.org/officials.aspx?report=u1')
        html_contents = response.read()
        # print html_contents
        soup = BeautifulSoup( html_contents,"html.parser" )
        # print soup.find("div", {'id': 'secondary_col2'})
        data = []
        for add in soup.findAll("div", {'class': 'candidate-cell-inner'}):
            d= (add.get_text('|',strip=True).encode("ascii",'ignore')).split('|') 
            data.append([d[1],d[5],d[0],d[2],d[4]])
        # print data
        data=[[(j.strip()).capitalize() for j in i] for i in data]
        with open('.\\Federal\\Fed_President_Vise.csv','wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","Age","Designation","Party","Website_url"])
            for row in data:
                csv_out.writerow(row)



        with open('.\\Federal\\Fed_President_Vise.csv','rb') as out:
            dddd = []
            data=csv.DictReader(out)
            # print data
            for i in data:
                dddd.append(i)
            # print d
            push_data.for_President_vise(dddd)
            print "pushed"

    except Exception, e:
        logger.error("Prasident and vise Description:"+str(e))


