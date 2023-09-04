from bs4 import BeautifulSoup
import os
import csv
# import csv
import re
import urllib2

import sys

# The wget module
import wget

# The selenium module
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

def get_mayor():
       # custom-2630-particle

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
    response = opener.open("http://www.northbrunswicknj.gov/mayor-council/mayor")
    html_contents = response.read()
    soup1 = BeautifulSoup( html_contents,"html.parser" )

    d = soup1.find('div',{"id":'custom-2630-particle'})

    email_mayor= (d.find('a')["href"]).split(':')[1]
    print email_mayor
    

    text= d.get_text('|',strip=True).encode('ascii','ignore')
    # print text
    p_name=(text.split(' ',1)[1]).split('|')[0]
    print p_name
    desi = (text.split(' ',1)[0])
    address = ','.join((text.split(' ',1)[1]).split('|')[1:-1])+', Email:'+email_mayor
    print desi
    print address


    return ([p_name,desi,address])



def Process(url,Dir,type_of,name,data_type,District):


    try:
        data_list = []
        s_extra=[name,type_of,"District-"+District]
        
        mayor_data = get_mayor()
        mayor_data = s_extra+mayor_data

        data_list.append(mayor_data)
        path = os.getcwd()


        chrome_path="C:\iamhere\chromedriver.exe"
        driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
        driver.get(url) # load the web page
        src = (driver.page_source).encode('ascii','ignore')
        with open (os.path.join(os.path.join(path,Dir),name+data_type+'.txt'),'w') as f:
            f.write(src)
        driver.close()
        with open(os.path.join(os.path.join(path,Dir),name+data_type+'.txt'),'r') as f:
            data=f.read()
        os.remove(os.path.join(os.path.join(path,Dir),name+data_type+'.txt'))
        soup = BeautifulSoup( data,"html.parser")

        # town='Old Bridge Township'
        
        table =soup.findAll('p', style=re.compile(r'text-align: center;'))
        
        address = ((soup.find('div', {'id': "custom-2630-particle"})).get_text(',',strip=True).encode('ascii','ignore')).replace('Contact Information',' ')
        print address
        # data_list = []
        for row in table:
            
            sublist=[]
            if "President" in (row.find("strong")).get_text():

                email=((row.find("a", text=re.compile('E-mail')))['href']).split(':')[1]
                # print email
                text = (row.find("strong")).get_text()
                # print text
                name_p=text.split(' ',2)[1]
                desi=text.split(' ',2)[0]
                sublist.append(name_p)
                sublist.append(desi)
                sublist.append(address.strip(' ,')+', Email:'+email)
                sublist=s_extra+sublist
                data_list.append(sublist)

            else:

                email=((row.find("a", text=re.compile('E-mail')))['href']).split(':')[1]
                # print email
                text = (row.find("strong")).get_text()
                # print text
                name_p=text.split(' ',1)[1]
                desi=text.split(' ',1)[0]

                sublist.append(name_p)
                sublist.append(desi)
                # print address
                sublist.append(address.strip(' ,')+', Email:'+email)
                sublist=s_extra+sublist
                data_list.append(sublist)


        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]

                # write.writerow(s)
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
    

# try:

#         Process("http://www.northbrunswicknj.gov/mayor-council/council", "Council","Township","North Brunswick ","Council",'17')

# except Exception, e:
#     print str(e)