from bs4 import BeautifulSoup
import os
import csv
# import csv
import re
import urllib2

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
        # print html_contents
        soup = BeautifulSoup( html_contents,"html.parser" )


        response1 = opener.open("http://www.oldbridge.com/content/5452/default.aspx")
        html_contents1 = response1.read()
        # print html_contents
        soup1 = BeautifulSoup( html_contents1,"html.parser" )

        mayor_name= ((soup1.find("div",{"class":"mayor clearfix"}).get_text(' ',strip=True).encode("ascii",'ignore')).split('Sincerely,')[1]).split('Mayor')[0]
        desi_mayo = "Moyor"




        town='Old Bridge Township'
        table = soup.find('table', {'class': "table table-striped imaged"})
        phone = (soup.find('table', {'class': "ContentTemp_2Column"})).get_text(' ',strip=True).encode("ascii",'ignore')
        phone= (phone.split('Contact Information')[1]).split('\n',1)[0]
        # print phone


        data_list=[]
        data_list.append(s_extra+[mayor_name,desi_mayo,""])
        print data_list


        for row in table.find_all('tr'):

            s=row.get_text('|',strip=True).encode('ascii','ignore').replace("|E-Mail","")

          
            s=s.split('|')
            if len(s)==2:
                email=row.find("a", text=re.compile('E-Mail'))
                email = email['href']

                s_extra=[name,type_of,"District-"+District]
                s=s_extra+s
                s.append("Email:"+email.split(':')[1]+','+phone)
                data_list.append(s)
        
                # write.writerow(s)
          
            elif len(s)==3:
                email=row.find("a", text=re.compile('E-Mail'))
                email = email['href']

                # print "in3"
                s_new=s[1:]
                
                s_new[1]=s_new[1]+','+s[0]
                s_extra=[name,type_of,"District-"+District]
                s = s_extra+s_new
                s.append("Email:"+email.split(':')[1]+','+phone)
                data_list.append(s)

            data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
            print  data_list
            b_set = set(map(tuple,data_list))  #need to convert the inner lists to tuples so they are hashable
            data_list = map(list,b_set) #Now convert tuples back into lists (maybe unnecessary?)


        # print data_list
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
            

        return 'Success'
    except Exception,e:
        logger.error(name+', '+data_type+", Description:"+str(e))
        print str(e)
# Process("http://www.oldbridge.com/content/5144/5243/default.aspx", "Council","Township","Oldbridge","Council","12")
