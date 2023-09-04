import urllib2
from bs4 import BeautifulSoup
import os
import csv
from db_module import push_data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from itertools import izip
import time 

import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

def Process(url,Dir,type_of,name,data_type,District):
    try:
        path=os.getcwd()
        s_extra=[name,type_of,"District-"+District]
        chrome_path="C:\iamhere\chromedriver.exe"
        driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
        driver.get(url) # load the web page
        # time.sleep(20)
        html_contents = (driver.page_source).encode('ascii','ignore')
        driver.close()
        soup = BeautifulSoup( html_contents,"html.parser" )

        div=soup.find('div', {'id': "content"})
        # print div
        ps = soup.findAll('p')
        missing_data= ps[3].get_text('|',strip=True).encode('ascii','ignore').split('|')[4:-1]

        data_list=[]
        data_list.append(s_extra+missing_data)
        for i  in ps[1:-1] :
            sub_list=[]

            i= i.get_text(',',strip=True).encode('ascii','ignore').split(',')[:4]
            print i

            if i[0]=="Mayor":
                i[0],i[1]=i[1],i[0]
                sub_list.append(i[0])
                sub_list.append(i[1]+','+i[2])
                sub_list.append("Email:"+i[3])
                sub_list = s_extra+sub_list
                data_list.append(sub_list)
   
            else:

                sub_list.append(i[0])
                sub_list.append(i[1])
                sub_list.append("Email:"+i[2])
                sub_list = s_extra+sub_list
                data_list.append(sub_list)

        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
        print data_list
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
            # print d
      
        # return 'Success'
    except Exception,e:
        logger.error(name+', '+data_type+", Description:"+str(e))

# Process("http://www.jamesburgborough.org/boroughcouncil.html", "Council","Township","Jamesburg","Council",'14')