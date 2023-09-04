import os
from bs4 import BeautifulSoup
import csv
import re
import string
import urllib2
from itertools import izip


# The wget module
import wget
from db_module import push_data
# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

def get_concil_memebrrs(url):

    path = os.getcwd()
    data_list = []
    chrome_path="C:\iamhere\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
    driver.get(url) # load the web page
    # time.sleep(20)
    html_contents = (driver.page_source).encode('ascii','ignore')
    driver.close()
    soup = BeautifulSoup( html_contents,"html.parser" )

    data_co = (((soup.find('div',{"id":'CityDirectoryLeftMargin'}).get_text('|',strip=True).encode('ascii','ignore')).split('|&lt;!')[0]).replace('Council|Title:','')).split('|')

    email = (str((soup.find('div',{"id":'CityDirectoryLeftMargin'})).findAll('a')[1]["href"])).split(':')[1]
    # print email
    data_list.append(email)
    # print type(email)
    # print email
    # print str(email).split(':')[1]
    # print type(data_co)
    # print data_list
    f = data_co+data_list
    
    
    # print '--------'
    return f


def get_mayor(url):

    path = os.getcwd()
    # data_list = []
    chrome_path="C:\iamhere\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
    driver.get(url) # load the web page
    # time.sleep(20)
    html_contents = (driver.page_source).encode('ascii','ignore')
    driver.close()
    soup = BeautifulSoup( html_contents,"html.parser" )

    name = soup.find('li',{"class":'widgetItem h-card'})
    raw =  (name.get_text( '|',strip=True).encode("ascii",'ignore')).split('|')
    print raw
    address = soup.find('div',{"class":'field h-adr'})
    address= (address.get_text( ' ',strip=True).encode("ascii",'ignore')).replace('Physical Address','')


    print address
    email = (name.find('a')['href']).split(':')[1]
    print email

    address = address+' Email:'+email+', '+raw[3]

    return ([raw[0],raw[1],address])




    
    # return f


def Process(url,Dir,type_of,name,data_type,District):

    try:
        base="http://www.twp.woodbridge.nj.us"
        data_list = []


        s_extra=[name,type_of,"District-"+District]
        path = os.getcwd()
        chrome_path="C:\iamhere\chromedriver.exe"
        driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
        driver.get(url) # load the web page
        # time.sleep(20)
        html_contents = (driver.page_source).encode('ascii','ignore')
        driver.close()
        soup = BeautifulSoup( html_contents,"html.parser")

        mayor_url = base+soup.find('a',{"class":'navMainItem secondaryNavItem withChildren'})['href']

        mayor_data = get_mayor(mayor_url)



        print mayor_url
        print '_________________________'

        data_list = []

        mayor_data = s_extra+mayor_data
        data_list.append(mayor_data)

        

        ul_tag = soup.findAll("ul")[4]
        ul_tag1 = soup.findAll("ul")[3]

        for li_tag in ul_tag.findAll("li"):
            anchor = (li_tag.find("a"))['href']
            data = get_concil_memebrrs(anchor)
            # print data
            data_list.append(s_extra+data)

        for li_tag in ul_tag1.findAll("li"):
            try:
                anchor = (li_tag.find("a"))['href']
                data = get_concil_memebrrs(anchor)
                print data
                # driver.Dispose()
            
                data_list.append(s_extra+data)
                
            except Exception, e:
                d =  (li_tag.get_text(' ',strip=True)).split(',')
                data_list.append(s_extra+d+[' '])
            print '--------'
        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
        # driver.Quit()
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
            print d
     
    except Exception, e:
        logger.error(name+', '+data_type+", Description:"+str(e))




# try:
#     Process("http://www.twp.woodbridge.nj.us/340/Council", "Council","Township","Woodbridge","Council","19")
# except Exception, e:
#     print str(e)


