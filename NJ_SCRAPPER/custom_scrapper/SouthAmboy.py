# import os
# from bs4 import BeautifulSoup
# import csv
# import re
# import string
# import urllib2
# from itertools import izip
# # from db_module import push_data

# # The wget module
# import wget

# # The selenium module
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import logging
# logger = logging.getLogger('myapp')
# hdlr = logging.FileHandler('myapp.log')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr) 
# logger.setLevel(logging.WARNING)
# import time
# def get_concil_memebrrs(url):

#     # s_extra=[name,type_of,"District-"+District]
#     path = os.getcwd()
#     opener = urllib2.build_opener()
#     opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
#     response = opener.open(url)
#     html_contents = response.read()
#     soup = BeautifulSoup( html_contents,"html.parser" )

    
#     soup = BeautifulSoup( html_contents,"html.parser" )
#     # time.sleep(20)
#     print 'in'

#     data = soup.find('ul',{"class":'contact-list'}).get_text('|',strip=True).encode('ascii','ignore')
#     print data
#     driver.close()


#     return data




# def Process(url,Dir,type_of,name,data_type,District):

#     try:
#         # data_list = []


#         s_extra=[name,type_of,"District-"+District]

#         final_lists = ["http://www.southamboynj.gov/Officials/Bio/mayor-fred-henry","http://www.southamboynj.gov/Officials/Bio/1st-ward-councilman-brian-mclaughlin","http://www.southamboynj.gov/Officials/Bio/2nd-ward-councilman-thomas-b-reilly","http://www.southamboynj.gov/Officials/Bio/3rd-ward-councilwoman-zusette-dato","http://www.southamboynj.gov/Officials/Bio/3rd-ward-councilwoman-zusette-dato","http://www.southamboynj.gov/Officials/Bio/councilwoman-at-large-christine-noble","http://www.southamboynj.gov/Officials/Bio/council-president-michael-gross"]

#         for kid_url in final_lists:
#             path = os.getcwd()
#             chrome_path="C:\iamhere\chromedriver.exe"
#             driver = webdriver.Chrome(chrome_path)
#             kid_url = kid_url
#             driver.get(url)
#             html_contents = (driver.page_source).encode('ascii','ignore')
#             driver.close()
#             soup = BeautifulSoup( html_contents,"html.parser" )
#         #     data = (get_concil_memebrrs(kid_url))
#         #     print data
#         #     data_list.append(s_extra+[data[1],data[0],','.join(data[2:])])
#         # data_list=[[j.strip() for j in i] for i in data_list]
#         # print data_list
#         # with open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'wb') as out:
#         #     csv_out=csv.writer(out) 
#         #     csv_out.writerow(["Name","type",'District',"person name","designation","Contact details"])   
#         #     for row in data_list:
#         #         csv_out.writerow(row)

#         # with open(os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv'), 'rb') as out:
#         #     d = []
#         #     data=csv.DictReader(out)
#         #     # print data
#         #     for i in data:
#         #         d.append(i)
#         #     # print d
#         #     push_data.now(d)
#         #     print os.path.join(os.path.join(path,Dir.strip()),"Township_"+name.strip()+'.csv') 
#             # print d


    
#     except Exception, e:
#         logger.error(name+', '+data_type+", Description:"+str(e))
# # Process("http://www.southamboynj.gov/", "Council","City","South Amboy","Council","19")





