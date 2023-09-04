import urllib2
from bs4 import BeautifulSoup
import time
# import xlrd
import re
import string
import os
import csv
from db_module import push_data

import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

def get_contact_info(url):
        # s_extra=[name,type_of,"District-"+District]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        data= (soup.find('font',{"class":'textstyle1'})).get_text('|',strip=True).encode('ascii','ignore')
        # print data

        return data




def Process(url,Dir,type_of,name,data_type,District):

    try:
        data_list=[]
        # base_url=url
        s_extra=[name,type_of,"District-"+District]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        table= soup.findAll('table')[12]

        

        for td_tag in table.findAll('td'):

            text = td_tag.get_text('|',strip=True).encode('ascii','ignore')
            # print text
            kid_url = '/'.join(url.split('/',)[:-1])+'/'+td_tag.find('a')["href"]
            # print kid_url
            other = get_contact_info(kid_url)
            contact = ','.join(other.split('|')[:-2]) +', '+''.join(other.split('|')[-2:])
            # print other
            print contact

            p_name = text.split('|')[0]
            p_desi = text.split('|')[1]

            data_list.append(s_extra+[p_name,p_desi,contact])


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

        # return 'Failed'

# Process("http://www.helmettaboro.com/Cit-e-Access/TownCouncil/?TID=102&TPID=10557", "Council","Borough","Helmetta","Council",'18')