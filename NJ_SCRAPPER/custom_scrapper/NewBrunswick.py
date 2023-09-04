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
        s_extra=[name,type_of,"District-"+District]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )

        mayor_data = (soup.findAll('div', {'class': 'textwidget'})[0]).get_text('|',strip=True).encode('ascii','ignore')
        mayor = mayor_data.split('|')[0]
        print mayor

        address_raw = soup.find('div', {'id': "copyright"})
        address_p_tag = address_raw.findAll('p')[0]
        address = (address_p_tag.get_text('|',strip=True).encode('ascii','ignore')).split('|')[0]
        print address


        table = soup.find('section', {'class': 'entry'})  #class="entry"
        data = soup.findAll('p')[4] 
        data = data.get_text('|',strip=True).encode('ascii','ignore').split('|')
        data = [(i.replace('*','')).strip() for i in data]
        print data
        data_list=[]
        mayor_list=s_extra+[mayor,"Mayor",address]
        data_list.append(mayor_list)


        for i in data:
            sub_list=[]
            if "President" in i:
                i=i.split('President')
                sub_list.append(i[1])
                sub_list.append(i[0]+" President")
                sub_list.append(address)
                sub_list=s_extra+sub_list
                data_list.append(sub_list)
            elif "Member" in i:
                i=i.split('Member')
                sub_list.append(i[1])
                sub_list.append(i[0]+" Member")
                sub_list.append(address)
                sub_list=s_extra+sub_list
                data_list.append(sub_list)


        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
        with  open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'wb') as out:
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
#     Process("http://thecityofnewbrunswick.org/city-council/","Council","City","New Brunswick","Council",'17')
# except Exception, e:
#     print str(e)


