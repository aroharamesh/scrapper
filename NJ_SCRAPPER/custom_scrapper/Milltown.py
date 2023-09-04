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
        s_extra=[name,type_of,"District-"+District]

        path = os.getcwd()
        chrome_path="C:\iamhere\chromedriver.exe"
        driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
        driver.get(url) # load the web page
        src = (driver.page_source).encode('ascii','ignore')
        soup = BeautifulSoup( src,"html.parser" )
        driver.close()

        links = soup.findAll('a',{"class":"glink"})[0]
        mayor_name= links.get_text('|',strip=True).encode('ascii','ignore')
        data_list = []

        data_list.append(s_extra+[mayor_name,"Mayor",'Email: '+links["href"].split(':')[1]])
        # print data_list
       

            # a_tags = list(set([ (i.get_text('|',strip=True).encode('ascii','ignore'),i["href"])  for i in soup.findAll("a", text=re.compile('Mayor'))]))
        Councilman = list(set([(i.get_text('|',strip=True).encode('ascii','ignore'),(i["href"]).split(':')[1]) for i in soup.findAll("a",{"class":"glink"}, text=re.compile('Councilman'))]))
        Councilwoman= list(set([(i.get_text('|',strip=True).encode('ascii','ignore'),(i["href"]).split(':')[1]) for i in soup.findAll("a",{"class":"glink"}, text=re.compile('Councilwoman'))]))
        Council_President= list(set([(i.get_text('|',strip=True).encode('ascii','ignore'),(i["href"]).split(':')[1]) for i in soup.findAll("a",{"class":"glink"}, text=re.compile('Council President'))]))

        # print a_tags
        # print Councilman
        # print Councilwoman
        # print Council_President

        for i in Councilman+Councilwoman:
            Desi =  i[0].split(' ',1)[0]
            # print desi
            name_p = (i[0].split(' ',1)[1]).split('-')[0]
            print name_p, Desi    

            data_list.append(s_extra+[name_p,Desi,"Email: "+i[1]])        
        # print data_list
        for i in data_list:
            print i
       
        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
        #         # print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
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
        logger.error(name+', '+data_type+", Description:"+str(e))

# Process("http://www.milltownnj.org/municipal/", "Council","Township","Milltown","Council",'17')       