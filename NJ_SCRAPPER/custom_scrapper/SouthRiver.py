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
import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)




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
        # main=soup.find('div', {'class': "field-item even"})
        table=soup.findAll('table')[4]
        mayor_data= (table.findAll('div',{'align':"center"})[1].get_text('|',strip=True).encode('ascii','ignore')).split('|')
        data_list.append(s_extra+[mayor_data[-1],mayor_data[0],''])
        
        for i in table.findAll('div',{'align':"center"})[3:]:

            raw= (i.get_text('|',strip=True).encode('ascii','ignore')).split('|')
            name = raw[-1]
            desi = ' '.join(raw[:-1])
            data_list.append(s_extra+[name,desi,''])


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
   
    except Exception, e:
        print str(e)




# try:
#     Process("http://www.southrivernj.org/elected_officials.html", "Council","Borough","South River","Council","18")
# except Exception, e:
#     print str(e)

