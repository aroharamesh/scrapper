import urllib2
from bs4 import BeautifulSoup
import time
# import xlrd
import re
import string
import os
import csv
from db_module import push_data

import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

import converter_southbro


from custom_scrapper import converter_southbro

# print converter_southbro.Process()


# import urllib2
# import os 
p = os.getcwd()

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import re



def pdf_to_txt():

    filedata = urllib2.urlopen('http://www.southbrunswicknj.gov/images/council/MayorCouncil2018a.pdf')  
    datatowrite = filedata.read()

    with open(os.path.join(os.path.join(p,"raw_files_pdf"),"MayorCouncil_southbrunswicknj.pdf"), 'wb') as f:  
        f.write(datatowrite)
    try:
        file_pointer = open(os.path.join(os.path.join(p,"raw_files_pdf"),"MayorCouncil_southbrunswicknj.pdf"), 'rb')

        # Setting up pdf reader
        pdf_resource_manager = PDFResourceManager()
        return_string = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(pdf_resource_manager, return_string, codec=codec, \
          laparams=laparams)
        interpreter = PDFPageInterpreter(pdf_resource_manager, device)

        for page in PDFPage.get_pages(file_pointer, set(), maxpages=0, password="",
          caching=True, check_extractable=True):
          interpreter.process_page(page)
        file_pointer.close()
        device.close()


        pdf_txt = return_string.getvalue()
        return_string.close()


        pdf_txt = pdf_txt.replace("\r", "\n")
        # pdf_txt = re.sub(regex.bullet, " ", pdf_txt)
        # print pdf_txt

        return pdf_txt.decode('ascii', errors='ignore')
    except Exception as e:
        print str(e)
        

def Process1():

    data_list=[]

    data= pdf_to_txt()
    d =data.split('which are listed on our site telephone directory.')[1]
    # print d.

    s= d.replace('\n', '').replace('\r', '').replace("Email",'').replace("2018",'|').replace("2020",'|').replace('-','')
    s= s.split("|")[:-1]
    # print s

    for i in [s[0],s[2],s[3],s[-1]]:
        i= (i.strip()).split(' ')
        # print i
        name = ' '.join(i[:-2])
        desi = i[-2]
        data_list.append([name,desi])
        # print data_list   
    # for i in data_list:
    #   print i
    #   print '-----'

    # print s[1]
    data_list.append([' '.join((s[1].strip()).split(' ')[:2]),' '.join((s[1].strip()).split(' ')[-3:-1])])

    return data_list




def Process(url,Dir,type_of,name,data_type,District):

    try:
        data_list=[]
        # base_url=url
        s_extra=[name,type_of,"District-"+District]
        path = os.getcwd()
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        div = soup.find("div",{'class':'body sec_summary'})
        table= soup.find('table')
        # data_list = []
        pdf_data= Process1()
        # print '---------------------------'
        # print pdf_data
        # print '---------------------------'
        sub_list = []

        for td_tag in table.findAll('tr'):

            text = td_tag.get_text('|',strip=True).encode('ascii','ignore')
                        

            if "Mayor" in text or "Councilman" in text or "Councilwoman" in text:

                m = text.split('|')[0]
                n = text.split('|')[-1]
                # print m , n
                sub_list.append([m,n])

            else:
                pass

        print pdf_data
        print '------'
        print sub_list

        for i in pdf_data:
            for j in sub_list:
                # d=""
                if   (i[0].split(' ')[-1]).lower() in  (j[0]).lower():
                    print "yes"
                    d = j[1]
                    # data_list.append(j+[d])
                    
                else:
                    print "no"
                    pass
            data_list.append(s_extra+[j.replace('"',' ') for  j in i]+["Phone: "+d])



        # print len(data_list)



        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
        print data_list

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
      
         
    except Exception, e:
        logger.error(name+', '+data_type+", Description:"+str(e))

        # return 'Failed'body sec_summary

# Process("http://www.southbrunswicknj.gov/directory", "Council","Township","South Brunswick","Council",'16')