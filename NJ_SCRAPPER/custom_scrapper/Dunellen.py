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
    return izip(a, a)




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

        div_tag = soup.find('div',{'class':'post'})
        print div_tag.get_text('|',strip=True).encode('ascii','ignore')
        data=div_tag.findAll('p')[:4]
        print data
        data_list=[]

        p1 = (data[0].get_text('|',strip=True).encode('ascii','ignore')).split('|')
        p2 = data[1].get_text('|',strip=True).encode('ascii','ignore')
        p3 = data[2].get_text('|',strip=True).encode('ascii','ignore')
        p4 = data[3].get_text('|',strip=True).encode('ascii','ignore')



        data_list.append([p1[0].split(' ',1)[1],p1[0].split(' ',1)[0],p1[1]])
        # print data_list
        data_list.append([p1[3].split('President')[1],p1[3].split('President')[0]+"President","Email: "+p1[4]+', phone: '+p1[5]])
        # print data_list
        data_list.append([p3.split('|')[0],'',p3.split('|')[1]])

        # print data_list
        print p3
    
        for i,j in pairwise(p2.split('|')[:2]+p2.split('|')[3:5]+p2.split('|')[7:9]+p2.split('|')[10:13]):
            data_list.append([i,'',j])


        data_list = [s_extra+i  for i in data_list]
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




# try:
#     Process("http://www.dunellen-nj.gov/government/mayor_and_council/index.php#.Wk3loN-Wa01", "Council","Borough","Dunellen","Council","22")
# except Exception, e:
#     print str(e)