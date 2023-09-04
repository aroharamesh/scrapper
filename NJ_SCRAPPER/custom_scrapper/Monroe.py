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
    path = os.getcwd()


    chrome_path="C:\iamhere\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
    driver.get(url) # load the web page
    src = (driver.page_source).encode('ascii','ignore')
    with open ('raw.txt','w') as f:
        f.write(src)
    driver.close()
    try:
        names_list=[]

        with open('raw.txt','r') as f:
            data=f.read()

        table = BeautifulSoup( data,"html.parser")
        # print table
        os.remove('raw.txt')

        missing_name=table.find("div", {'id': 'printReady'})
        
        names= table.findAll('h4')
        for i in names :

            names_list.append(i.get_text('', strip=True).encode('ascii', 'ignore'))

        for i in missing_name.findAll('p'):
            i= (i.get_text('|', strip=True).encode('ascii', 'ignore'))
            if  "Councilwoman" in i and len(i)<30:
                # print i
                names_list.append(i)
            else:
                pass
        
        emails= table.findAll("a", text=re.compile('Email'))
        emails=[(em.get("href").split(':')[1]).split('?')[0] for em in emails]
  
        names_list_ele=names_list[0].split()

   
        names_list[-1],names_list[-2]=names_list[-2],names_list[-1]
        final_data_list=[]
        extr_data=[name,type_of,"District-"+District]
        for i,j in zip(names_list,emails):
            sublist=[]
            if "Mayor" in i:


                desi=i.split(' ',1)[0]
                name_p = i.split(' ',1)[1]
                # print name,desi,j
                sublist.append(name_p)
                sublist.append(desi)
                sublist.append('Email:'+j)
                sublist=extr_data+sublist
                final_data_list.append(sublist)

            else:
                print '-----'
                print i
                try:
                    name_p=i.split(',')[0]
                    desi = i.split(',')[1]
                    
                except Exception, e:
                    name_p=i.split(' ',1)[1]
                    desi = i.split(' ',1)[0]




                # print name,desi,j
                sublist.append(name_p)
                sublist.append(desi)
                sublist.append('Email:'+j)
                sublist=extr_data+sublist
                final_data_list.append(sublist)
        # print final_data_list

        final_data_list=[[(j.strip()).capitalize() for j in i] for i in final_data_list]
        with open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'wb') as out:

            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type",'District',"person name","designation","Contact details"])
            for row in final_data_list:
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
            # print d
      

        return 'Success'
    except Exception,e:
        logger.error(name+', '+data_type+", Description:"+str(e))
        
# Process("http://www.monroetwp.com/township_council.cfm", "Council","Township","Monroe","Council",'14')