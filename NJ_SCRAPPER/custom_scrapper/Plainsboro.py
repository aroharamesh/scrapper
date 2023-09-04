import urllib2
from bs4 import BeautifulSoup
import time
import re
import string
import os
import csv
import sys
from db_module import push_data
import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)



def get_more_data(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
    response = opener.open(url)
    html_contents = response.read()
    soup = BeautifulSoup( html_contents,"html.parser" )

    dat = soup.findAll('div',{'class':"widget editor pageStyles narrow"})[1]

    email = soup.find('a',text=('email'))

    return (dat.get_text('|',strip=True).encode('ascii','ignore')).split('|')+[email["href"]]



def Process(url,Dir,type_of,name,data_type,District):

    try:

        data_list=[]
        s_extra=[name,type_of,"District-"+District]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        dat = soup.findAll('div',{'class':"widget editor pageStyles narrow"})[1]


        for a_tag in dat.findAll('a'):


            try:
                
                kid_url = '/'.join(url.split('/')[:-2])+'/'+a_tag['href']
                # print kid_url
                data=get_more_data(kid_url)
                data_list.append(s_extra+data[:2]+[data[3]+', Email:'+data[4].split(':')[1]])

                
            except Exception, e:

                kid_url = a_tag['href']

                data=get_more_data(kid_url)
                data_list.append(s_extra+data[:2]+[data[3]+', Email:'+data[4].split(':')[1]])

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
       

# Process("http://www.plainsboronj.com/309/Mayor-Township-Committee", "Council","Township","Plainsboro","Council",'14')
