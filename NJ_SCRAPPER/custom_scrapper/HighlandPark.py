from bs4 import BeautifulSoup
import os
import urllib2

import sys
import csv
import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)
# The wget module
import wget
from db_module import push_data
# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
def Process(url,Dir,type_of,name,data_type,District):
    path = os.getcwd()

    chrome_path="C:\iamhere\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
    driver.get(url) # load the web page
    src = (driver.page_source).encode('ascii','ignore')
    driver.close()

    soup = BeautifulSoup( src,"html.parser" )
    address = soup.find('div', {'id': 'CityDirectoryLeftMargin'})
    ps=address.findAll('p')
    ps=[p.get_text("|", strip=True).encode('ascii','ignore') for p in ps]
    print ps


    try:
        town = 'Highland Park'
        town1 = 'HighlandParkCouncilMembers'
        datasets=[]
        table = soup.find('table', {'summary': 'City Directory'}) 
        tr=table.find_all('tr')
        trs=tr[2:]
        main_list=[]
        for row in trs :
            s_extra=[name,type_of,"District-"+District]
            sub_list=[]
            data = row.get_text("|", strip=True)
            raw= data.split('\n')
            # print raw
            text=raw[0]
            email_phone=raw[-1]
            name_p=text.split('|')[0]
            desi = text.split('|')[1]
            sub_list.append(name_p)
            sub_list.append(desi)
            sub_list.append(ps[0]+', Phone:'+ps[1]+', Fax:'+ps[2]+', Email:'+email_phone.split('|')[1])
            sub_list=s_extra+sub_list
            main_list.append(sub_list)
           
        # print main_list
        main_list=[[(j.strip()).capitalize() for j in i] for i in main_list]
        with open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type",'District',"person name","designation","Contact details"])
            for row in main_list:
                csv_out.writerow(row)

        with open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'rb') as out:
            d = []
            data=csv.DictReader(out)
            # print data
            for i in data:
                d.append(i)
            # print d
            push_data.now(d)
            # print os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv') 
            # print d
      

        return 'Success'
    except Exception, e:
        logger.error(name+', '+data_type+", Description:"+str(e))
# Process("http://www.hpboro.com/Directory.aspx?DID=32", "Council","Borough","Highland Park","Council",'18')
