import os
from bs4 import BeautifulSoup
import csv
import re
import string
import urllib2
from itertools import izip
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)



def Process(url,Dir,type_of,name,data_type):
    try:
        base_url=url.split('/')
        base_url = '/'.join(base_url[:-1])

        s_extra=[name,type_of]
        path = os.getcwd()
        chrome_path="C:\iamhere\chromedriver.exe"
        driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
        driver.get(url) # load the web page
        html_contents = (driver.page_source).encode('ascii','ignore')
        soup = BeautifulSoup( html_contents,"html.parser" )

        driver.close()



        table = soup.findAll('table',{'width':'100%',"border":"0","cellspacing":"0","cellpadding":"0"})[1]
        table_2= table.findAll("table",{'width':'100%',"border":"0","cellspacing":"0","cellpadding":"0"})[-1]
        # print table_2
        dept_names_list=(table_2.findAll("font",{'class':'textstyle3'}))
        dept_names_list = [x.get_text('',strip=True).encode('ascii','ignore')  for x in dept_names_list ]

        


        table_2= table.find("table",{'width':'100%',"border":"0","cellspacing":"3","cellpadding":"0"})#.get_text('|',strip=True).encode('ascii','ignore')

        data_list=[]
        for i in table_2.findAll("tr"):
            sub_list=[]
            a=  (i.get_text('|',strip=True).encode('ascii','ignore')).split('|')
            if len(a)>2 and 'Phone' not in a:
                print len(a), a
                if "Tel" in a[1] or "Fax" in a[1] : 
                    p_name=a[0]
                    desi = ''
                    address = ','.join(a[1:])
                    sub_list.append(p_name)
                    sub_list.append(desi)
                    sub_list.append(address)

                    sub_list= s_extra+sub_list
                    data_list.append(sub_list)
                else:
                    p_name=a[0]
                    desi = a[1]
                    address = ','.join(a[2:])
                    sub_list.append(p_name)
                    sub_list.append(desi)
                    sub_list.append(address)
                    
                    sub_list= s_extra+sub_list
                    data_list.append(sub_list)



            else:
                pass

        with open(os.path.join(os.path.join(path,Dir),name+data_type+'.csv'), 'wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type","person name","designation","Contact details"])    
            for row in data_list:
                csv_out.writerow(row)


   
    except Exception, e:
        print str(e)




try:
    Process("http://www.sayreville.com/Cit-e-Access/ContactInfo/?TID=87&TPID=8641", "Departments","Borough","Sayreville","Departments")
except Exception, e:
    print str(e)