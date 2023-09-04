import os
from bs4 import BeautifulSoup
import csv
import re
import string
import urllib2
from itertools import izip


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a, a, a)

def pairwise1(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a, a)


def Process(url,Dir,type_of,name,data_type):
    try:
        base_url=url.split('/')
        base_url = '/'.join(base_url[:-1])

        s_extra=[name,type_of]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )

        table = soup.findAll('table')[0]
        # print table
        raw_data=(table.get_text('|',strip=True).encode('ascii','ignore')).split('|')
        # print len(raw_data)
        data_list=[]
        for w, x ,y ,z  in pairwise(raw_data[:24]+raw_data[29:64]+raw_data[65:68]+raw_data[70:77]+raw_data[87:90]+raw_data[95:98]):
            sub_list=[]
            print w,x,y,z
            dept_name=w
            p_name=dept_name
            p_desi=' '
            address= x+','+y+','+z
            # sub_list.append(dept_name)
            sub_list.append(p_name)
            sub_list.append(p_desi)
            sub_list.append(address)
            sub_list=s_extra+sub_list
            data_list.append(sub_list)
            
        with open(os.path.join(os.path.join(path,Dir),name+data_type+'.csv'), 'wb') as out:
            csv_out=csv.writer(out) 
            csv_out.writerow(["Name","type","person name","designation","Contact details"])   
            for row in data_list:
                csv_out.writerow(row)






   
    except Exception, e:
        print str(e)




try:
    Process("http://thecityofnewbrunswick.org/directory/", "Departments","Township","New Brunswick","Departments")
except Exception, e:
    print str(e)