 # Council Member
import urllib2
from bs4 import BeautifulSoup
import os
import csv

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
from itertools import izip
import time 
import re
from db_module import push_data
def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a, a)
# http://www.metuchennj.org/metnj/GOVERNMENT/Mayor/


def get_mayor_data ():

    path = os.getcwd()
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
    response = opener.open("http://www.metuchennj.org/metnj/GOVERNMENT/Mayor/")
    html_contents = response.read()
    soup = BeautifulSoup( html_contents,"html.parser" )

    mayor_data= (soup.find("strong",text=re.compile('Mayor'))).get_text('',strip=True).encode('ascii','ignore')
    mayor_email= (soup.find("a", href=lambda href: href and "mailto:" in href)).get_text('',strip=True).encode('ascii','ignore')
    data = mayor_data.split(',')+[mayor_email]

    # print data
    # print mayor_email
    return data


def Process(url,Dir,type_of,name,data_type,District):
    try:
        path=os.getcwd()
        data_list=[]
        s_extra=[name,type_of,"District-"+District]
        chrome_path="C:\iamhere\chromedriver.exe"
        driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
        driver.get(url) # load the web page
        # time.sleep(20)
        html_contents = (driver.page_source).encode('ascii','ignore')
        driver.close()
        soup = BeautifulSoup( html_contents,"html.parser" )

        d = soup.findAll('table')[6]
        # print d[6]
        # print len(d)
        for i in d.findAll('tr'):
        	# print i
        	data= (i.find('p').get_text('|',strip=True).encode('ascii','ignore')).split('|')
        	data_list.append(s_extra+[data[1],data[0],','.join(data[-2:])])

        	# print i.find('a').get_text('|',strip=True).encode('ascii','ignore')
        # data= ((d.get_text('|',strip=True).encode('ascii','ignore')).split('|Council Member|Term Expires|E-Mail Address|')[1]).split('|Borough Council Meeting Date')[0]
        # # print data
        # for i , j , k in pairwise(data.split('|')):
        # 	# print i, k
        # 	if "Council President" in i:
        # 		i = i.split('--')
        # 		data_list.append(s_extra+i+[k])
        # 	else:
        # 		data_list.append(s_extra+[i,"Council Member",k])
        # print data_list
        # data_list.append(s_extra+get_mayor_data())
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
        return 'Success'
    except Exception,e:
        logger.error(name+', '+data_type+", Description:"+str(e))
        print str(e)
        return 'Failed'

# Process("http://www.southplainfieldnj.com/spnj/Mayor%20%26%20Council/", "Council","Borough","South Plainfield","Council",'18')


# South Plainfield	Borough	Council	18	http://www.southplainfieldnj.com/spnj/Mayor%20%26%20Council/   	Opens only in AWS instance						
