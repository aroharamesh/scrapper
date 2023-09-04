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

def get_concil_memebrrs_email (url):

    path = os.getcwd()
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
    response = opener.open(url)
    html_contents = response.read()
    soup = BeautifulSoup( html_contents,"html.parser" )

    prasident_email= (soup.findAll("a", href=lambda href: href and "mailto:" in href))[0].get_text('',strip=True).encode('ascii','ignore')

    return prasident_email


def get_mayor(kid_url):

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
    response = opener.open(kid_url)
    html_contents = response.read()
    soup = BeautifulSoup( html_contents,"html.parser" )

    d = soup.find('span',{"class":'subheader'})
    p_name = d.get_text('',strip=True).encode('ascii','ignore')
    # print p_name
    p_desi = p_name.split(' ',1)[0]

    p_name = p_name.split(' ',1)[1]

    
    mayor_email= soup.findAll("a", href=lambda href: href and "Mailto:" in href)
    # print mayor_email

    p_email = mayor_email[0].get_text('',strip=True).encode('ascii','ignore')

    


    return ([p_name,p_desi,p_email])






def Process(url,Dir,type_of,name,data_type,District):

    try:


        s_extra=[name,type_of,"District-"+District]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )

        data_list = []
        mayor_url= soup.find("a", text=re.compile('Mayor'))
        print mayor_url
        mayor_url = '/'.join(url.split('/',)[:-3])+'/'+mayor_url['href']
        mayor_data=get_mayor(mayor_url)



        data_list.append(s_extra+[mayor_data[0],mayor_data[1],mayor_data[2]])


        ul_tag = soup.findAll('ul')[-1]
        # print ul_tag
        for li_tag in ul_tag.findAll('a'):
            # print li_tag
            kid_url= '/'.join(url.split('/',)[:-3])+'/'+li_tag['href']
            p_text= li_tag.get_text('|',strip=True)
            # print p_text
            if len(p_text.split(',')) > 1:
                p_desi = p_text.split(',')[1]
                p_name = p_text.split(',')[0]
            else :
                p_desi = ''
                p_name = p_text
            # print p_name,p_desi

            email = get_concil_memebrrs_email(kid_url)


            data_list.append(s_extra+[p_name,p_desi,email])
        # print data_list

        left_off = (ul_tag.findAll('li')[-1]).get_text('|',strip=True).encode('ascii','ignore')
    
        data_list.append(s_extra+[left_off,'',''])
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
#     Process("http://www.edisonnj.org/departments/council/council_members.php", "Council","Township","Edison","Council","18")
# except Exception, e:
#     print str(e)