import os
from bs4 import BeautifulSoup
import csv
import re
import string
import urllib2
from itertools import izip
from db_module import push_data

import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a, a, a)



def Process(url,Dir,type_of,name,data_type,District):

    try:
         

        base_url=url.split('/')
        base_url = '/'.join(base_url[:-1])

        s_extra=[name,type_of,"District-"+District]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )

        table = soup.findAll('table')[0]
        td_text= table.find("td").get_text('|',strip=True).encode('ascii','ignore')
        text = td_text.split('|Members / Phone Number /|Term Expires|')[1]


        data_list=[]

        for p_name,p_desi,phone_no,other in pairwise(text.split('|')[:8]+text.split('|')[11:]+(text.split('|')[8:10])+["",""]):
            sub_list=[]
            sub_list=[p_name.strip(','),p_desi,phone_no]
            sub_list = s_extra+sub_list
            data_list.append(sub_list)


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
        

    # finally:
        




# try:
#     Process("http://www.carteret.net/content/2855/3390/default.aspx", "Council","Borough"," Carteret","Council","19")
# except Exception, e:
#     print str(e)