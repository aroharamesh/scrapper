import os
from bs4 import BeautifulSoup
import csv
import re
import string
import urllib2


def Process(url,Dir,type_of,name,data_type):
    try:
        delete_list=['Facebook','Police Department Facebook Page','Contact Us','Directory',"Email the Clerk's Office","Email Engineering",'More Information','Directions','Physical Address']

        base_url=url.split('/')
        base_url = '/'.join(base_url[:-2])


        s_extra=[name,type_of]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )

        ol_tag = soup.find('ol', {'class': 'semanticList layout2', 'role': 'menu'})

        data_list=[]
        for li_tag in ol_tag.findAll('li')[:-6]:
            sub_list=[]
            next_link= li_tag.find('a')["href"]
            dept_name= li_tag.find('a').get_text()

            kid_url=base_url+next_link

            response_kid = opener.open(kid_url)
            html_contents_kid = response_kid.read()
            soup_kid = BeautifulSoup( html_contents_kid,"html.parser" )

            data=[s.extract() for s in soup_kid.findAll(['script', 'style'])]
            data = soup_kid.find('aside',{'class':'secondaryContent',"data-cprole":"contentContainer",'id':'featureColumn'})

            data1= data.get_text('|',strip=True).encode('ascii','ignore')

            data2=data1.split('|Directory|')[0]

            if data2.split('|')[1]==dept_name or dept_name.split(' ')[0] in data2.split('|')[1]:

                p_name=' '
                p_desi=' '
                address= ' '.join([x for x in data2.split('|') if x not in delete_list])

                sub_list.append(p_name)
                sub_list.append(p_desi)
                sub_list.append(address)
                sub_list=s_extra+sub_list
                print len(sub_list),sub_list
                data_list.append(sub_list)

            else:
                data4=([x for x in data2.split('|') if x not in delete_list])
                # print data4
                p_name=data4[0]
                p_desi=data4[1]
                address = ' '.join(data4[3:])

                sub_list.append(p_name)
                sub_list.append(p_desi)
                sub_list.append(address)
                sub_list=s_extra+sub_list
                print len(sub_list),sub_list
                data_list.append(sub_list)

        with open(os.path.join(os.path.join(path,Dir),name+data_type+'.csv'), 'wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(["Name","type","person name","designation","Contact details"])
            for row in data_list:
                csv_out.writerow(row)
               


    except Exception, e:
        print str(e)




try:
    Process("http://www.twp.woodbridge.nj.us/148/Departments", "Departments","Township","Woodbridge","Departments")
except Exception, e:
    print str(e)