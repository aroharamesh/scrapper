from bs4 import BeautifulSoup
import time
import re
import string
import os
import urllib2
import csv 




def Process(url,Dir,type_of,name_t,data_type):
    try:
        s_extra=[name_t,type_of]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        # width: 900px; height: 1290px; margin-right: auto; margin-left: auto;
        soup = BeautifulSoup( html_contents,"html.parser" )

        table = soup.findAll('table')[1]
        # print table
        data_list=[]
        for tr_tags in table.findAll('tr')[1:]:
            sub_list=[]
            p_name = (tr_tags.findAll('td')[0]).get_text(' ',strip=True).encode('ascii','ignore')

            phone = (tr_tags.findAll('td')[1]).get_text(' ',strip=True).encode('ascii','ignore')

            desi=''

            # print dept_name,phone
            sub_list.append(p_name)
            sub_list.append(desi)
            sub_list.append(phone)
            sub_list=s_extra+sub_list
            print sub_list
            data_list.append(sub_list)


        with open(os.path.join(os.path.join(path,Dir),name_t+data_type+'.csv'), 'wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type","person name","designation","Contact details"]) 
            for row in data_list:
                csv_out.writerow(row)



    
   
    except Exception, e:
        print str(e)
        return 'Failed'




try:
    Process("http://www.piscatawaynj.org/contacts/contact-us", "Departments","Township","Piscataway","Departments")
except Exception, e:
    print str(e)