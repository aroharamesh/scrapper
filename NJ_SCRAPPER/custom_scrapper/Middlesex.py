import urllib2
from bs4 import BeautifulSoup
import time
# import xlrd
import re
import string
import os
import csv
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
    return izip(a, a, a, a, a)




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
        table= soup.find('ul',{"class":'slides'})
        data= table.findAll('li')[:2]
        # print data
        mayor_data = (data[0].get_text('|',strip=True).encode('ascii','ignore')).split('|')[:5]
        # print mayor_data
        # print '-'

        data_list.append(s_extra+[mayor_data[0].split(' ',1)[1],mayor_data[0].split(' ',1)[0],':'.join(mayor_data[1:3])+', '+':'.join(mayor_data[3:5])])
        # print data_list

        consil_data = (data[1].get_text('|',strip=True).encode('ascii','ignore')).split('|')
        # print consil_data

        for name_desi,p,no,e,e_id in pairwise(consil_data):
            print [name_desi,p,no,e,e_id]

            if "Council President" in name_desi:
                p_name = name_desi.split(' ',2)[2]
                p_desi =  ' '.join((name_desi.split(' ',2)[0:2]))

                data_list.append(s_extra+[p_name,p_desi,p+no+', '+e+e_id])
          
            else:
                p_name = name_desi.split(' ',1)[1]
                p_desi =  (name_desi.split(' ',1)[0])
                # print p_desi
                # print p_name
                data_list.append(s_extra+[p_name,p_desi,p+no+', '+e+e_id])

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
        

# Process("http://www.middlesexboro-nj.gov/index.php/get-involved/contact-us", "Council","Borough","Middlesex","Council",'22')