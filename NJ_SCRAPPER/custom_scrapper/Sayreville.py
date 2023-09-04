import os
from bs4 import BeautifulSoup
import csv
import re
import string
import urllib2
from itertools import izip

from db_module import push_data

import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_concil_memebrrs_email (url):

    path = os.getcwd() 
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
    response = opener.open(url)
    html_contents = response.read()
    soup = BeautifulSoup( html_contents,"html.parser" )

    prasident_email= (soup.findAll("a", href=lambda href: href and "mailto:" in href))[0].get_text('',strip=True).encode('ascii','ignore')

    return prasident_email


def get_mayor(kid_url):

    chrome_path="C:\iamhere\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
    driver.get(kid_url) # load the web page
    html_contents = (driver.page_source).encode('ascii','ignore')
    soup = BeautifulSoup( html_contents,"html.parser" )



    d = (soup.findAll('p')[2])
    # print d
    # print d
    driver.close()

    p_name1 = d.get_text('',strip=True).encode('ascii','ignore')
    # print p_name
    # p_desi = "Mayor"

    p_desi = 'Mayor'
    p_name = (p_name1.split(' '))[1]
    # print p_name[1]

    
    mayor_email= soup.findAll("a", href=lambda href: href and "mailto:" in href)[0]
    print mayor_email

    p_email = (mayor_email['href']).split(':')[1]
    print p_email
    # p_email = 

    


    return ([p_name,p_desi,p_email])






def Process(url,Dir,type_of,name,data_type,District):

    try:


        s_extra=[name,type_of,"District-"+District]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )

        data_list = []
        mayo = get_mayor('http://www.sayreville.com/cit-e-access/webpage.cfm?TID=87&TPID=8879')
        data_list.append(s_extra+mayo)

        table = soup.findAll('table')[13]
        # print table[13]
        for td_tag in table.findAll('td'):
            td_data= (td_tag.get_text('|',strip=True)).split('|')
            print '----------------'



            data_list.append(s_extra+td_data[:2]+[' '])

            print data_list

        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
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
      
   
    except Exception, e:
        logger.error(name+', '+data_type+", Description:"+str(e))




# try:
#     Process("http://www.sayreville.com/Cit-e-Access/TownCouncil/?TID=87&TPID=8636", "Council","Borough","Sayreville","Council","19")
# except Exception, e:
#     print str(e)

