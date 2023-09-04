from bs4 import BeautifulSoup
import os
import csv
# import csv
import re
import urllib2

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from db_module import push_data
import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)


# def get_data():

def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return 'ntg'

def Process(url,Dir,type_of,name,data_type):


    try:
        s_extra=[name,Dir]
        base_url=url.split('/')
        base_url = '/'.join(base_url[:-2])
        print base_url
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        # print html_contents
        soup = BeautifulSoup( html_contents,"html.parser" )
        # print soup
        ref = ['12','14','16','17','18','19','22']

        a_tags = soup.findAll('a',text=re.compile('Legislators for District'))

        a_tags = [ (i["href"]).encode('ascii','ignore') for i in a_tags]

        # print a_tags
        sub_string = 'OCCUPATION'
        Assembly_data_list=[]
        Senator_data_list=[]
        for a in a_tags:
            for r in ref:
                if r in a:
                    kid_url= base_url+a.strip('.')
                    # response_kid = opener.open(kid_url)
                    # src = response_kid.read()
                    chrome_path="C:\iamhere\chromedriver.exe"
                    driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
                    driver.get(kid_url) # load the web page
                    time.sleep(3)
                    src = (driver.page_source).encode('ascii','ignore')
                    driver.close()
                    soup_kid = BeautifulSoup( src,"html.parser" )
                    # table_kid=soup.find('table')
                    table_kid=soup_kid.find('table')



                    for tr in table_kid.findAll('tr'):
                        sub_list=[]

                        if len(tr.findAll('td'))==2 :
                            name_text= (tr.findAll('td')[0]).get_text('|',strip=True).encode('ascii','ignore')
                            add_other = (tr.findAll('td')[1]).get_text('|',strip=True).encode('ascii','ignore')
                            
                            address= (tr.findAll('i')[-1]).get_text('|',strip=True).encode('ascii','ignore')

                            OCCUPATION_index = index_containing_substring(add_other.split('|'),sub_string)

                            OCCUPATION = add_other.split('|')[OCCUPATION_index+1]

                            party=name_text.split('|')[0]

                            type_of_person = name_text.split('|')[1]

                            p_name = name_text.split('|')[2]

                            sub_list.append(type_of_person)
                            sub_list.append(party)
                            sub_list.append('District-'+str(r))
                            sub_list.append(p_name)
                            sub_list.append(OCCUPATION)
                            sub_list.append(address)

                            if "Senator" in sub_list[0]:
                                sub_list=s_extra+sub_list
                                Senator_data_list.append(sub_list)

                            elif "Assembly" in sub_list[0]:
                                sub_list=s_extra+sub_list
                                Assembly_data_list.append(sub_list)                                




                            print '------------'


                        else:
                            pass




                else:
                    pass


                
                # write.writerow(s)
        Senator_data_list=[[(j.strip()).capitalize() for j in i] for i in Senator_data_list]
        with open(os.path.join(os.path.join(path,Dir),"State_"+'Senator.csv'), 'wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type","Designation","Party","District","Person name","Occupation","Contact"])
            for row in Senator_data_list:
                csv_out.writerow(row)
                
        Assembly_data_list=[[(j.strip()).capitalize() for j in i] for i in Assembly_data_list]
        with open(os.path.join(os.path.join(path,Dir),"State_"+'Assembly.csv'), 'wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type","Designation","Party","District","Person name","Occupation","Contact"])
            for row in Assembly_data_list:
                csv_out.writerow(row)


        with open(os.path.join(os.path.join(path,Dir),"State_"+'Senator.csv'), 'rb') as out:
            d = []
            data=csv.DictReader(out)
            # print data
            for i in data:
                d.append(i)
            # print d
            push_data.for_state_sen_assem(d)

        with open(os.path.join(os.path.join(path,Dir),"State_"+'Assembly.csv'), 'rb') as out:
            d = []
            data=csv.DictReader(out)
            # print data
            for i in data:
                d.append(i)
            # print d
            push_data.for_state_sen_assem(d)


        # return 'Success'
    except Exception,e:
        print str(e)
        logger.error(name+', '+data_type+", Description:"+str(e))




# try:
#     Process("http://www.njleg.state.nj.us/districts/districtnumbers.asp", "county","Middlesex","Middlesex","county")

# except Exception, e:
#     print str(e)
    # contentWrap