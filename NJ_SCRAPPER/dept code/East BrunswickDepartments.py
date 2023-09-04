import os
from bs4 import BeautifulSoup
import csv
import re
import string
import urllib2
from itertools import izip


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from itertools import izip
import time 
# def pairwise(iterable):
#     "s -> (s0, s1), (s2, s3), (s4, s5), ..."
#     a = iter(iterable)
#     return izip(a, a, a, a)

# def pairwise1(iterable):
#     "s -> (s0, s1), (s2, s3), (s4, s5), ..."
#     a = iter(iterable)
#     return izip(a, a, a)


def Process(url,Dir,type_of,name,data_type):
    try:
        base_url=url.split('/')
        base_url = '/'.join(base_url[:-2])
        print base_url

        s_extra=[name,type_of]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )

        div_tag = soup.find('div',{'class':'main wide grid_12 clearfix'})
        table = div_tag.find('table')
        data_list=[]
        for tr_tag in table.findAll('tr'):
            sub_list = []
            dept_name = ((tr_tag.findAll("td"))[0]).get_text(',',strip=True).encode('ascii','ignore')
            contact = ((tr_tag.findAll("td"))[1]).get_text(',',strip=True).encode('ascii','ignore')
            p_desi =''
            sub_list.append(dept_name)
            sub_list.append(p_desi)
            sub_list.append(contact)
            sub_list = s_extra+sub_list
            data_list.append(sub_list)
            
            
            # print dept_name,contact



            
        with open(os.path.join(os.path.join(path,Dir),name+data_type+'.csv'), 'wb') as out:
            csv_out=csv.writer(out) 
            csv_out.writerow(["Name","type","person name","designation","Contact details"])   
            for row in data_list:
                csv_out.writerow(row)






   
    except Exception, e:
        print str(e)




try:
    Process("https://www.eastbrunswick.org/content/202/default.aspx", "Departments","Township","East Brunswick","Departments")
except Exception, e:
    print str(e)
    contentWrap