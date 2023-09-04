import os
from bs4 import BeautifulSoup
import csv
import re
import string
import urllib2


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

        address=soup.find('div', {'class': "footer sixteen columns"})


        address= address.get_text(',',strip=True).encode('ascii','ignore')

        address= ','.join((address.split(',',3))[:3])
        # print table  
        data_list=[]

        for tr_tag in table.findAll('tr'):

            sub_list=[]

            td_tags=tr_tag.findAll('td')[1:]

            p_name_desi=td_tags[0].get_text('|',strip=True).encode('ascii','ignore')

            p_phone= td_tags[1].get_text(',',strip=True).encode('ascii','ignore')


            if len(p_name_desi)!=0 :
                text= p_name_desi.split('|')[0].split(',')

                
                if len(text) > 1:
                    name=text[0]
                    desi = ','.join(text[1:])

            
                    
                elif len(text) <=1:
                    name = text[0]
                    desi = ''

                if len(p_name_desi.split('|'))>1:
                    email_id= p_name_desi.split('|')[1]
                    # print email_id
                    p_phone = p_phone
                else:
                    email_id = ''
                    p_phone = p_phone

            address_final = address+','+email_id+','+p_phone
            print name,desi,address_final
            sub_list.append(name)
            sub_list.append(desi)
            sub_list.append(address_final)
            sub_list = s_extra+sub_list
            data_list.append(sub_list)


        with open(os.path.join(os.path.join(path,Dir),name_t+data_type+'.csv'), 'wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type","person name","designation","Contact details"]) 
            for row in data_list:
                csv_out.writerow(row)

        return 'Success'
    except Exception,e:
        print str(e)
        return 'Failed'



try:
    Process("http://www.dunellen-nj.gov/directory/index.php#.WkHzSt-Wa01", "Departments","Borough","Dunellen","Departments")
except Exception, e:
    print str(e)