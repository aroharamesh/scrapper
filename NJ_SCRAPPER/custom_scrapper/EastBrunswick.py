import urllib2
from bs4 import BeautifulSoup
import os
import csv
from db_module import push_data

from itertools import izip

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

def get_mayor():

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
    response = opener.open("https://www.eastbrunswick.org/content/202/271/default.aspx")
    html_contents = response.read()
    soup = BeautifulSoup( html_contents,"html.parser" )

    d = soup.find('div',{"class":'main wide grid_12 clearfix'})
    p_tag = d.findAll("p")[:2]
    data = [i.get_text('|',strip=True).encode('ascii','ignore') for i in p_tag]
    
    p_name = data[0].split('|')[1]
    p_desi = (data[0].split('|')[0]).strip(':')

    address = ','.join((data[1]).split('|'))

    return ([p_name,p_desi,address])


    # print d





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

        mayor_data = get_mayor()

        mayor_data = s_extra+mayor_data

        data_list.append(mayor_data)




        address=soup.findAll('div', {'class': "grid_4 alpha"})[-1]

        address= address.get_text(',',strip=True).encode('ascii','ignore')

        table=soup.find('table')

        data=table.get_text('|',strip=True).encode('ascii','ignore')

        data=data.split('|')
        

        for x, y in pairwise(data):
            sub_list=[]
            sub_list.append(x)
            sub_list.append(y)
            sub_list.append(address)
            sub_list=s_extra+sub_list
            data_list.append(sub_list)
        # print data_list
        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
        
        with open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type",'District',"person name","designation","Contact details"])
            for row in data_list:
                csv_out.writerow(row)


        with open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'rb') as out:
            ddd = []
            data=csv.DictReader(out)
            # print data
            for i in data:
                ddd.append(i)
            # print d
            push_data.now(ddd)
            print os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv') 
            # print d
      

        return 'Success'
    except Exception,e:
        logger.error(name+', '+data_type+", Description:"+str(e))
        

# Process("https://www.eastbrunswick.org/content/202/293/default.aspx", "Council","Township","East Brunswick","Council",'18')