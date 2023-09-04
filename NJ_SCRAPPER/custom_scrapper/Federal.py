'''
State elected officials (Governor, Lt. Governor, State Senators & Assemblymen)


http://www.middlesexcountynj.gov/Government/Pages/Federal-and-State-Officials-.aspx

'''

'''
Federal elected officials (for example, President, VP, Senators and Congressmen.
 
https://www.senate.gov/general/contact_information/senators_cfm.cfm

https://www.house.gov/representatives

'''
'''
School Board or Board of Education

https://homeroom5.doe.state.nj.us/directory/district.php

plainsborough

'''
import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

from db_module import push_data

import urllib2
from bs4 import BeautifulSoup
import cookielib
import re
import itertools
import os

import re
import csv

import itertools

# import get_address

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def Senators_of_the_115th_Congress():

    raw_data=""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open('https://www.senate.gov/general/contact_information/senators_cfm.cfm?State=NJ')
    html_contents = response.read()
    # print html_contents
    soup = BeautifulSoup( html_contents,"html.parser" )
    # print soup.find("div", {'id': 'secondary_col2'})
    for add in soup.findAll("div", {'id': 'secondary_col2'}):
        for i in soup.findAll("div", {"width" : "100%"}):
            content1 = (i.get_text('|', strip=True).encode('ascii', 'ignore'))
            # print content1
            raw_data=raw_data+content1
    data= raw_data.replace('|Contact:','')
    # print a

    data= list(grouper(6, data.split('|')))

    data_final=[]

    for i in data:
        i = list(i)
        i[1] =((i[1].split('(')[1]).strip(')'))
        i = tuple(i)
        data_final.append(i)
    print data_final
        
    data_final=[[j.strip() for j in i] for i in data_final]
    with open('Federal\\Fed_Senators.csv','wb') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(["Name","State","Class","Address","Contact Number","Conatct URL"])
        for row in data_final:
            csv_out.writerow(row)



    with open('Federal\\Fed_Senators.csv','rb') as out:
        dddd = []
        data=csv.DictReader(out)
        # print data
        for i in data:
            dddd.append(i)
        # print d
        push_data.for_Federal_Senators(dddd)
        print "pushed"
        
# try:
#     Senators_of_the_115th_Congress()
# except Exception, e:
#     print "something went wrong"
#     Senators_of_the_115th_Congress()


def get_address_of_congressmen(url):

    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    
    address_list=[]
    if url=="https://norcross.house.gov/" or url=="https://macarthur.house.gov/" or url=="https://lance.house.gov/" or url=="https://sires.house.gov/" or url=="https://pascrell.house.gov/":
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        all_adrees= soup.findAll("div", {'class': 'office-info'})
        for adress in all_adrees:
            adress=(adress.get_text(' ', strip=True).encode('ascii', 'ignore'))
            address_list.append(adress)
        return address_list

    elif url=="https://lobiondo.house.gov/" or url=="https://pallone.house.gov/" or url=="https://payne.house.gov/":
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        all_adrees= soup.findAll("div", {'id': 'sub-address'})
        for adress in all_adrees:
            adress=(adress.get_text(' ', strip=True).encode('ascii', 'ignore'))
            address_list.append(adress)
        return address_list

    elif url=="https://chrissmith.house.gov/":
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        footer=soup.find("div", {'class': 'footer-top'})
        all_adrees= footer.findAll("section", {'class': 'column'})
        for adress in all_adrees:
            adress=(adress.get_text(' ', strip=True).encode('ascii', 'ignore'))
            address_list.append(adress)
        return address_list

    elif url=="https://gottheimer.house.gov/":
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        # footer=soup.find("div", {'class': 'footer-top'})
        all_adrees= soup.find('ul', {'class': 'accordion'})
        for adress in all_adrees.find_all('li'):
            address=(adress.get_text(' ', strip=True).encode('ascii', 'ignore'))
            address_list.append(address)
        return address_list

    elif url=="https://watsoncoleman.house.gov/":
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        all_adrees=soup.findAll("address", {'class': 'col'})
        for adress in all_adrees:
            address=adress.get_text(' ', strip=True).encode('ascii', 'ignore')
            address_list.append(address)
        return address_list

    elif url=="https://frelinghuysen.house.gov/":
        url=url+"contact-us/"
        response = opener.open(url)
        html_contents = response.read()
        soup = BeautifulSoup( html_contents,"html.parser" )
        # s = soup.findAll("table", {"border": "0"})[-1].find("table")
        all_adrees=soup.find("div", {'class': 'itembody'})
        # print all_adrees
        p = all_adrees.findAll("p")

        address1=p[4].get_text(' ', strip=True).encode('ascii', 'ignore')
        address2 = p[5].get_text(' ', strip=True).encode('ascii', 'ignore')
        address_list.append(address1)
        address_list.append(address2)

        return address_list
    else:
        return address_list




def Congressmen():

    try:
        
    

        columns="State|District|Name|Party|Office Room|Phone|Committee Assignment|Address1|Address2|Address3|Address4|Address5|Address6"

        raw_data=""
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open('https://www.house.gov/representatives')
        html_contents = response.read()
        # print html_contents
        soup = BeautifulSoup( html_contents,"html.parser" )
        full= soup.find("div", {'class': 'view-content'})
        main_list=[]
        for table in full.findAll("table", {'class': 'table'}):
            # print table

            caption = table.find('caption')
            caption= caption.get_text(strip=True)
            # print caption
            tbody=table.find('tbody')
            tr=tbody.findAll('tr')


            if "New Jersey" in caption:

     
                for every in tr:
                    sub_list=[]
                    address_url= every.a.get('href')
                    address_url = address_url.rstrip("/")
                    address_url= address_url+"/"
                    print address_url
                  
                    each=(every.get_text('|', strip=True).encode('ascii', 'ignore'))
                    each=each.split('|')
                    sub_list.append(caption)
                    sub_list.append(each[0])
                    sub_list.append(each[1])
                    sub_list.append(each[2])
                    # main_list.append(caption)
                    sub_list.append(each[3])
                    sub_list.append(each[4])
                    address=get_address_of_congressmen(address_url)
                    # d= ' '.join(each[5:]
                    sub_list.append(' '.join(each[5:]))
                    sub_list=sub_list+address
                    main_list.append(sub_list)
                    # print main_list

        main_list=[[(j.strip()).capitalize() for j in i] for i in main_list]
        with open('Federal\\Fed_Representatives.csv','wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(columns.split('|'))
            for row in main_list:
                csv_out.writerow(row)

        with open('Federal\\Fed_Representatives.csv','rb') as out:
            dddd = []
            data=csv.DictReader(out)
            # print data
            for i in data:
                dddd.append(i)
            # print d
            push_data.for_Federal(dddd)
            print "pushed"
            
            # print d

    except Exception, e:
        logger.error("Federal, Representatives, Description:"+str(e))
      





# try:
#     Congressmen()
# except Exception, e:
#     print "something went wrong "
#     Congressmen()

import re
def New_Jersey_School_Directory():

    Municipals="Carteret,Cranbury,Dunellen,East Brunswick,Edison,Helmetta,Highland Park,Jamesburg,Metuchen,Middlesex Borough,Milltown,Monroe,New Brunswick,North Brunswick,Old Bridge,Perth Amboy,Piscataway,Plainsboro,Sayreville,South Amboy,South Brunswick,South Plainfield,South River,Spotswood,Woodbridge"
    column ="County name(county code),Distict name(dist code),Municipal_name,address,official name1,official_title1,official phone1,official email1,Official Name2,Official Title2,Official Phone with .ext2,Official Name3,Official Title3,Official Phone with .ext3,Official Name4,Official Title4,Official Phone with .ext4,Official Name5,Official Title5,Official Phone with .ext5,Official Name6,Official Title6,Official Phone with .ext6,Official Name7,Official Title7,Official Phone with .ext7"

    try:

        import requests
        requests.packages.urllib3.disable_warnings()

        import ssl

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            # Legacy Python that doesn't verify HTTPS certificates by default
            pass
        else:
            # Handle target environment that doesn't support HTTPS verification
            ssl._create_default_https_context = _create_unverified_https_context


        raw_data=""
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open('https://homeroom5.doe.state.nj.us/directory/district.php')
        html_contents = response.read()
        # print html_contents
        soup = BeautifulSoup( html_contents,"html.parser" )
        # print soup.find("div", {'id': 'secondary_col2'})

        data_list=[]
        
        for add in soup.findAll("div", {'class': 'district_box'}):

            sub_list=[]
            
            d = add.get_text('|',strip=True).encode('ascii','ignore')
            
            if "Middlesex County" in d or 'plainsboro' in d:
           

                raw = filter(None, d.split('|')[6:])

                if raw[0]=='List Schools':

                    raw = raw[1:]

                    county_name = raw[0]
                    district_name = raw[1]
                    address = ','.join(raw[2:4])
                    sub_list.append(county_name)
                    sub_list.append(district_name)

                    Municipals_name_list=[]

                    for x in Municipals.split(','):
                        


                        if x.lower() in district_name.lower():
                            Municipal_name=x
                            Municipals_name_list.append(Municipal_name)
                        elif x.lower() in address.lower():
                            Municipal_name=x
                            Municipals_name_list.append(Municipal_name)
                        else:
                            pass

                    sub_list.append(Municipals_name_list[0])



                      #dummy
                    sub_list.append(address)
                    table = add.find("table")

                    tr = table.findAll("tr")
                    content2 = (tr[0].get_text('|', strip=True).encode('ascii', 'ignore'))

                    name_title=content2.split('|')
                    name=name_title[0].split(',')[0]
                    title = name_title[0].split(',')[1]
                    phone=name_title[1]
                    email=name_title[2]
                    sub_list.append(name)
                    sub_list.append(title)
                    sub_list.append(phone)
                    sub_list.append(email)
                    for j in tr[1:]:
                        print j 
                        content3 = (j.get_text('|', strip=True).encode('ascii', 'ignore'))
                        name_title1=content3.split('|')
                        name1=name_title1[0].split(',')[0]
                        title1= name_title1[0].split(',')[1]
                        phone1=name_title[1]
                        # email=name_title[2]
                        sub_list.append(name1)
                        sub_list.append(title1)
                        sub_list.append(phone1)
                   
                    print sub_list
                    data_list.append(sub_list)



                else:
                    raw = raw
                    county_name = raw[0]
                    district_name = raw[1]
                    address = ','.join(raw[2:4])
                    sub_list.append(county_name)
                    sub_list.append(district_name)

                    for x in Municipals.split(','):
                        if x.lower() in district_name.lower():
                            Municipal_name=x
                            sub_list.append(Municipal_name)
                        elif x.lower() in address.lower():
                            Municipal_name=x
                            sub_list.append(Municipal_name)
                        else:
                            pass


                    # sub_list.append(Municipal_name)
                    sub_list.append(address)
                    table = add.find("table")
                    tr = table.findAll("tr")
                    content2 = (tr[0].get_text('|', strip=True).encode('ascii', 'ignore'))
                    name_title=content2.split('|')
                    name=name_title[0].split(',')[0]
                    title = name_title[0].split(',')[1]
                    phone=name_title[1]
                    email=name_title[2]
                    sub_list.append(name)
                    sub_list.append(title)
                    sub_list.append(phone)
                    sub_list.append(email)
                    for j in tr[1:]:
                        content3 = (j.get_text('|', strip=True).encode('ascii', 'ignore'))
                        name_title1=content3.split('|')
                        name1=name_title1[0].split(',')[0]
                        title1= name_title1[0].split(',')[1]
                        phone1=name_title[1]
                        # email=name_title[2]
                        sub_list.append(name1)
                        sub_list.append(title1)
                        sub_list.append(phone1)
                   
                    print sub_list
                    data_list.append(sub_list)

        # print data_list
        # print len(data_list)
        # print data_list


        data_list=[[(j.strip()).capitalize() for j in i] for i in data_list]
        for i in data_list :
            print i
        with open('State\\State_school_board.csv','wb') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(column.split(','))
            for row in data_list:
                csv_out.writerow(row)



        with open('State\\State_school_board.csv','rb') as out:
            dddd = []
            data=csv.DictReader(out)
                # print data
            for i in data:
                dddd.append(i)
                # print d
            push_data.State_school_board(dddd)
            print "pushed"

    except Exception as e:
        logger.error("Federal, Representatives, Description:"+str(e))

# New_Jersey_School_Directory()





# import re, unicodedata

# import string

# def get_Senate_and_Assembly():

#     columns="State|Name|Title|Party|Address1|Address2|Address3|Address4"

#     raw_data=""
#     opener = urllib2.build_opener()
#     opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#     response = opener.open('http://www.njleg.state.nj.us/members/abcroster.asp')
#     html_contents = response.read()
#     # print html_contents
#     soup = BeautifulSoup( html_contents,"html.parser" )
#     full= soup.findAll("table", {'width': '100%'})
#     all_data =(soup.get_text('|', strip=True).encode('utf-8'))
#     data_1=all_data.split("Jersey Senate and Assembly Alphabetical List of Members")
#     data_2=data_1[1].strip()
#     data_ass=data_2.split("|Assemblyman",1)[1]
#     data_san=data_2.split("|Assemblyman",1)[0]




#     data_3= data_san.split("|Senator")
#     sanetor=[]

#     for i in data_3:
#         s_sub_list=[]                                                                           
#         a_sub_list=[]
#         if len(i)!= 0:
#             i= re.sub(r'[\xc2,\xa0]+', " ", i)
#             sanetor_d = (i.split('|'))
#             sanetor_d = filter(None, sanetor_d)
#             s_sub_list.append("New Jersey")    
#             s_sub_list.append(sanetor_d[0])
#             s_sub_list.append("Senator")
#             s_sub_list.append(sanetor_d[1])
#             s_sub_list=s_sub_list+sanetor_d[4:]
#             sanetor.append(s_sub_list)

    

#     data_4= data_ass.split("|Assemblyman")

    
#     Assembly=[]
#     for j in data_4:
      
                                                                                 
#         a_sub_list=[]
        

#         if len(i)!= 0:
#             j= re.sub(r'[\xc2,\xa0]+', " ", j)
#             Assemblyman_d = (j.split('|'))
#             print Assemblyman_d
  
#             Assemblyman_d = filter(None, Assemblyman_d)

#             if len(Assemblyman_d)>=11:
 
#                 alt_1='|'.join(Assemblyman_d)
       
#                 alt_2 = alt_1.split("|Assembly")
 
#                 for i in alt_2:
#                     if i.split('|')[0]=='woman':
#                         i=i.split('|')
#                         i=i[1:]
#                         a=[]

#                         a.append("New Jersey")    
#                         a.append(i[0])
#                         a.append("Assemblywoman")
#                         a.append(i[1])
#                         a=a+i[4:]
#                         Assembly.append(a) 

#                     else:
#                         i=i.split('|')
#                         b=[]

                    
#                         b.append("New Jersey")    
#                         b.append(i[0])
#                         b.append("Assemblyman")
#                         b.append(i[1])
                   
#                         b=b+i[4:]
#                         Assembly.append(b)                        

#             else:
  
#                 a_sub_list.append("New Jersey")    
#                 a_sub_list.append(Assemblyman_d[0])
#                 a_sub_list.append("Assemblyman")
#                 a_sub_list.append(Assemblyman_d[1])
#                 a_sub_list=a_sub_list+Assemblyman_d[4:]
#                 Assembly.append(a_sub_list)

               

 
    
#     with open('State\\State_Senate.csv','wb') as out:
#         csv_out=csv.writer(out)
#         csv_out.writerow(columns.split('|'))
#         for row in sanetor:
#             csv_out.writerow(row)


    
#     with open('State\\State_Assemblyman.csv','wb') as out:
#         csv_out=csv.writer(out)
#         csv_out.writerow(columns.split('|'))
#         for row in Assembly:
#             csv_out.writerow(row)


# get_Senate_and_Assembly()