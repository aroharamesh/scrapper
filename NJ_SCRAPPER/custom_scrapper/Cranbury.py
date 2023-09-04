from bs4 import BeautifulSoup
import csv
import os
import urllib2
import sys
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
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        # print html_contents
        soup = BeautifulSoup( html_contents,"html.parser" )


        table = soup.find_all("table")[-1]

        data_list=[]
        s_extra=[name,type_of,"District-"+District]
        for row in table.find_all('tr'):

            data = row.get_text(",", strip=True)
            
            try:
                email = row.find('a')
                email1 = email['href'].encode('ascii', 'ignore')
                print email1
                data = data +', Email:' + email1
                # print data
                data = data.replace('mailto:', '')
                data = data.split(',')
                # print data
        
                del data[2]
                # print data
                data=s_extra+data
                # print data
                
                data_list.append(data)
                # print data_list
                

            except Exception, e:
                pass
        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
                # print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
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
            # print ds
          
      
   
        return 'Success'
    except Exception, e:
        logger.error(name+', '+data_type+", Description:"+str(e))

# Process("http://cranburytownship.org/twp_committee.html", "Council","Township","Cranbury","Council",'14')