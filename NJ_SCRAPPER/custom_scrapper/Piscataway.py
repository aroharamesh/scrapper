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

def Process(url,Dir,type_of,name,data_type,District):
    try:
        
        s_extra=[name,type_of,"District-"+District]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        main=soup.find('div', {'class': "field-item even"})
        table=main.find('table')
        data_list=[]
        for i in table.findAll('td'):
            sub_list=[]
            text=(i.get_text('|',strip=True).encode('ascii','ignore')).split("|")
            # print text
            name_p=text[0]
            desi=text[1]
            address=text[-2:]
            
            sub_list.append(name_p)
            sub_list.append(desi)
            sub_list.append(address[0]+", Phone:"+address[-1])
            sub_list=s_extra+sub_list
            data_list.append(sub_list)

        with open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'wb') as out:
            print os.path.join(os.path.join(path,Dir),name+data_type+'.csv')
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type",'District',"person name","designation","Contact details"])
            for row in data_list:
                csv_out.writerow(row)
        print data_list
        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
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
    except Exception, e:
        logger.error(name+', '+data_type+", Description:"+str(e))



# Process("http://www.piscatawaynj.org/admin_dept/mayor-township-council", "Council","Township","Piscataway","Council",'17')






