import os
from bs4 import BeautifulSoup
import csv
import urllib2
import re
import time

import sys

# The wget module
import wget
from db_module import push_data
# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import urllib.request

import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)


def Process(url,Dir,type_of,name,data_type,District):
    try:
        data_list=[]
        s_extra=[name,type_of,"District-"+District]

        path = os.getcwd()
        chrome_path="C:\iamhere\chromedriver.exe"
        driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
        driver.get(url) # load the web page
        src = (driver.page_source).encode('ascii','ignore')
        soup = BeautifulSoup( src,"html.parser" )
        driver.close()

        Mayor_data = soup.find("font",text=re.compile('Mayor')).get_text('|',strip=True).encode('ascii','ignore')
        print Mayor_data
        data_list.append(s_extra+[Mayor_data.split(' ',1)[1],Mayor_data.split(' ',1)[0],''])
        # print data_list 


        Councilman_data = soup.findAll("table",{'bgcolor':"#FFFFFF"})[-1]
        # print Councilman_data

        for i in Councilman_data.findAll('tr'):
            d = (i.get_text('|',strip=True).encode('ascii','ignore')).split('|')
            if "Council President" in d[0]:
                data_list.append(s_extra+[d[0].split('President')[1],"Council President","Email: "+d[1]])
            else:
                data_list.append(s_extra+[d[0].split(' ',1)[1],d[0].split(' ',1)[0],"Email: "+d[1]])
        for i in data_list:
            print i


           
       
       
        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
                # print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        with open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type",'District',"person name","designation","Contact details"])
            for row in data_list:
                csv_out.writerow(row)

        
        with open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'rb') as out:
            d = []
            data=csv.DictReader(out)
            # print data
            for i in data:
                d.append(i)
            # print d
            push_data.now(d)
            print os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv') 
            # print ds
          
      
   
        return 'Success'
    except Exception, e:
        print str(e)
        logger.error(name+', '+data_type+", Description:"+str(e))

# Process("http://www.spotswoodboro.com/council.html", "Council","Township","Spotswood","Council",'14')       