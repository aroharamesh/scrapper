import os
from bs4 import BeautifulSoup
import csv
import re
import string
import urllib2
from itertools import izip


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from itertools import izip
import time 
# def pairwise(iterable):
#     "s -> (s0, s1), (s2, s3), (s4, s5), ..."
#     a = iter(iterable)
#     return izip(a, a, a, a)

# def pairwise1(iterable):
#     "s -> (s0, s1), (s2, s3), (s4, s5), ..."
#     a = iter(iterable)
#     return izip(a, a, a)


def Process(url,Dir,type_of,name,data_type):
    try:
        base_url=url.split('/')
        base_url = '/'.join(base_url[:-2])
        print base_url

        s_extra=[name,type_of]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )

        div_tag = soup.find('div',{'class':'contentWrap'})
        a_tags=div_tag.findAll('a')[2:]
        a_tags = [base_url+i['href'] for i in a_tags]
        data_list = []
        #link in a_tags[:6]+a_tags[7:10]+a_tags[11:]:
        for  link in a_tags[:6]+a_tags[7:10]+a_tags[11:]:
            sub_list=[]
            # print link
            chrome_path="C:\iamhere\chromedriver.exe"
            driver = webdriver.Chrome(chrome_path) # if you want to use chrome, replace Firefox() with Chrome()
            driver.get(link) # load the web page
            html_contents = (driver.page_source).encode('ascii','ignore')
            driver.close()
            soup = BeautifulSoup( html_contents,"html.parser" )
            try:
         
                div_tag= soup.find('div',{'class':'pageContent cpGrid cpGrid24 showInMobile'})

                try:
                   
                    p_name=div_tag.find('h4',{'class':'widgetTitle field p-name'}).get_text(' ',strip=True).encode('ascii','ignore')
                    # print p_name

                except Exception, e:
                    print str(e)

                    p_name=''
                


                try:
                   
                    p_desi = div_tag.find('div',{'class':'field p-job-title'}).get_text(' ',strip=True).encode('ascii','ignore')
                    # print p_desi

                except Exception, e:
                    print str(e)

                    p_desi=''

            
                try:
                   
                
                    id_raw = div_tag.find('div',{'class':'field u-email'})
                    email_id = id_raw.find('a')
                    # print email_id
                    email_id = ((email_id['href']).encode('ascii','ignore')).split(':')[1] 
                    # print email_id
                except Exception, e:
                    print str(e)

                    email_id=''
                except Exception, e:
                    id_raw = div_tag.find('div',{'class':'field u-email'})
                    email_id = id_raw.findAll('a')[1]
                    # print email_id
                    email_id = ((email_id['href']).encode('ascii','ignore')).split(':')[1] 
                    # print email_id




                try:
               
                    p_address = div_tag.find('div',{'field h-adr'}).get_text(' ',strip=True).encode('ascii','ignore')
                    # print p_address
                except Exception, e:

                    p_address=''
                    print str(e)



                try:
               
                    p_tel = div_tag.find('div',{'field p-tel'}).get_text(' ',strip=True).encode('ascii','ignore')
                    # print p_tel
                except Exception, e:

                    p_tel=''
                    print str(e)

                try:
               
                    p_Fax = div_tag.find('div',{'class':'field'},text=re.compile('Fax')).get_text(' ',strip=True).encode('ascii','ignore')
                    print p_Fax
                except Exception, e:

                    p_Fax=''
                    print str(e)


                # print p_name,p_desi,email_id,p_address,p_tel
                sub_list.append(p_name)
                sub_list.append(p_desi)
                sub_list.append(p_address+', Email:'+email_id+','+p_tel+','+p_Fax)
                sub_list = s_extra+sub_list
                print sub_list
                print '------------------'
                data_list.append(sub_list)

            except Exception, e:
                print str(e)
                pass
            
            
        with open(os.path.join(os.path.join(path,Dir),name+data_type+'.csv'), 'wb') as out:
            csv_out=csv.writer(out) 
            csv_out.writerow(["Name","type","person name","designation","Contact details"])   
            for row in data_list:
                csv_out.writerow(row)






   
    except Exception, e:
        print str(e)




try:
    Process("http://www.plainsboronj.com/148/Departments", "Departments","Township","Plainsboro","Departments")
except Exception, e:
    print str(e)
    contentWrap