import re
from bs4 import BeautifulSoup
import os
import urllib2
import csv 
from db_module import push_data


import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)
def Process(url,Dir,type_of,name,data_type):
  

    try:
        s_extra=[name,type_of]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )

        data_list=[]
        for member in soup.findAll("div",{'class':"contact-info"}):
            sublist=[]

            data= member.get_text('|',strip=True).encode('ascii','ignore')
            sublist = [data.split("|")[0],data.split("|")[1]]
            sublist = s_extra+sublist
            data_list.append(sublist)

       
        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
        with open(os.path.join(os.path.join(path,Dir.strip()),"County_"+name.strip()+'.csv'), 'wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type","person name","designation"])
            for row in data_list:
                csv_out.writerow(row)
        with open(os.path.join(os.path.join(path,Dir.strip()),"County_"+name.strip()+'.csv'), 'rb') as out:
            ddd = []
            data=csv.DictReader(out)
            # print data
            for i in data:
                ddd.append(i)
            # print d
            push_data.for_Elected_officials(ddd)
            # print os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv') 
            # print d

        
    except Exception, e:
        logger.error(name+', '+data_type+", Description:"+str(e))
        print str(e)







