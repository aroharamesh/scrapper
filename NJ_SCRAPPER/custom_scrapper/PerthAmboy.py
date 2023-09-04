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
        council_link =((soup.findAll("a", text=re.compile('Council'))))
        mayor_data = soup.findAll('a',text=re.compile('Mayor'))[1]
        council_link = [link.get_text('|',strip=True).encode('ascii','ignore') for link in council_link]
        council_link = council_link[1:-2]
        council_link.append(mayor_data.get_text('|',strip=True).encode('ascii','ignore'))
        print council_link
        
        for d in council_link:
            if "Council Member" in d:
                data_list.append(s_extra+[d.split(' ',2)[-1],' '.join(d.split(' ',2)[:-1]),''])
                # print data_list
                # print '--------------'
            elif "Councilman" in d or 'Mayor' in d:
                data_list.append(s_extra+[d.split(' ',1)[-1],d.split(' ',1)[0],''])

            else:
                pass


        print data_list

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

# Process("http://ci.perthamboy.nj.us/", "Council","City","Perth Amboy","Council",'19')