import urllib2
from bs4 import BeautifulSoup
import cookielib
import re
import itertools
import os
#E:\E-Directory Project\Automation Of E-Directory\Python_Files\Middlesex_directory_dept.py
import urllib2
from bs4 import BeautifulSoup
import cookielib
import re
import itertools
import os
#E:\E-Directory Project\Automation Of E-Directory\Python_Files\Middlesex_directory_dept.py
path = os.getcwd()
def final(path, Dir):
    try:
        os.remove(os.path.join(path, Dir + '.txt'))
    except:
        pass
    fhout = open(os.path.join(path, Dir + '.txt'), 'a')
    Fh = open(os.path.join(path, Dir + '5.txt'), 'r')
    for i in Fh:
        b = i.replace(',:,', ': ')
        c = b.replace('Phone Number:,', 'Phone Number:')

        d = c.replace('Fax:,', 'Fax:')

        e = d.replace('Fax -,', 'Fax-')
        f = e.replace('Click here to find out more about the Prosecutor', ' ')
        final = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ',f)

        print final
        print type(final)
        fhout.writelines(final)

    Fh.close()
    fhout.close()
    try:
        os.remove(os.path.join(path, Dir + '1.txt'))
        os.remove(os.path.join(path, Dir + '2.txt'))
        os.remove(os.path.join(path, Dir + '3.txt'))
        os.remove(os.path.join(path, Dir + '4.txt'))
        os.remove(os.path.join(path, Dir + '5.txt'))
    except Exception,e:
        pass

def format(path, Dir):
    try:
        try:
           os.remove(os.path.join(path, Dir + '5.txt'))
        except:
            pass
        data = []
        fh = open(os.path.join(path, Dir + '4.txt'), 'r')
        a = fh.read()
        fh.close()

        b = a.split('_______________________________')

        f = open(os.path.join(path, Dir + '5.txt'), 'a')
        for i in b:
            mystring = str(i)
            aa = mystring.split('|')
            aaa = filter(None, aa)

            str1 = ','.join(aaa)

            str2 = str1.split('\n')

            aaa = filter(None, str2)

            print aaa

            aaaa = ','.join(aaa)

            f.writelines(aaaa)

            f.writelines('\n')
        f.close()
        final(path, Dir)
        print 'Content been written to 6.content_County.txt'
        return 'Success'
    except Exception,e:
        print e
        return 'Failed'
def valid_data(path, Dir):
    try:
        os.remove(os.path.join(path, Dir + '4.txt'))
    except:
        pass
    print 'inside validdata'
    fin = open(os.path.join(path, Dir + '3.txt'), 'r')  # Function to Remove Unwanted  chunks of data from the whole dataset
    #fin = open("content.txt",'r')
    fout = open(os.path.join(path, Dir + '4.txt'), "w+")
    #fout = open("TRIAL1.txt", "w")
    delete_list = ['|Share', '|Facebook', '|Twitter', '|Google plus', '|Linkedin', '|Tumblr', '|Email', '|Print',
                   '|Contact me', '\r', '\t', ',', '\xc2\xa0\xc2\xa0\xc2\xa0', '\u00a0']
    for line in fin:
        print type(fin)
        for word in delete_list:
            a = re.sub(' +', ' ', line)
            line = a.replace(word, "")

        fout.write(line)
    fin.close()
    fout.close()
    format(path, Dir)
    print "CONTENT HAS BEEN WRITTEN TO 4.Content_Two.txt"


def crawl(path, Dir):
    print '#############################################################'
    try:
        os.remove(os.path.join(path, Dir + '3.txt'))
    except:
        pass

    try:

        delimeter = '_______________________________'  # Function to featch all content from the web page in an unstractured format and differentiate dept by delimeter____
        fh1 = open(os.path.join(path, Dir + '2.txt'),'r')
        for lin in iter(fh1):
            line = lin  # .encode('ascii','ignore')
            print line


            def grab(line,path, Dir):


                FH = open(os.path.join(path, Dir + '3.txt'),'a')

                url = line
                opener = urllib2.build_opener()
                opener.addheaders = [('user_agent', 'Chrome/43.0.2357.124')]  # grab the content and put it in a file
                response = opener.open(url)
                soup = BeautifulSoup(response)
                headding = soup.title.string
                FH.writelines(headding)

                for add in soup.findAll("div", {'class': 'col-xs-12'}):
                    content1 = (add.get_text('|', strip=True).encode('ascii', 'ignore'))
                    print content1

                    FH.writelines(content1)

                FH.writelines('\n' + delimeter + '\n')

                FH.close()

                valid_data(path, Dir)
            try:
                grab(line,path, Dir)
            except Exception, e:
                print str(e)
          

            
            print ('content has been saved in text file ')

        fh1.close()

        print 'Task Completed'
        print 'content been written to the text file 3.content.txt'
        #valid_data(path, Dir)
    except:
        fh1.close()
    print '#############################################################'




def AlterLInk(path, Dir):
    try:
        os.remove(os.path.join(path, Dir + '2.txt'))
    except:
        pass
    try:
        print 'inside alter link'


        with open(os.path.join(path, Dir + '1.txt'), 'r') as selectedlinks:

            li = selectedlinks.read()
            opener = urllib2.build_opener()
            opener.addheaders = [('user_agent', 'Chrome/43.0.2357.124')]
            try:
                links = re.findall('(https?://\S+)', li)  # final all http and https links
                for link in links:
                    # print link


                    if 'aspx' in link:  # Find all .aspx  valied links
                        with open(os.path.join(path, Dir + '2.txt'), 'a') as FHfinal:
                        # print link

                            FHfinal.writelines(link + '\n')
            except Exception, e:
                print str(e)
        crawl(path, Dir)

    except Exception, e:
        print str(e)


def Process(url,Dir,type_of,name,data_type):


                

    try:

        with open(os.path.join(path, Dir + '1.txt'), 'a') as FH:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
            response = opener.open(url)
            html_contents = response.read()
            soup = BeautifulSoup( html_contents,"html.parser")
            baseurl = "http://www.co.middlesex.nj.us"
            headding = soup.title.string
            print headding
            data = soup.findAll('div', attrs={'class': 'animsition'})
            for div in data:
                links = div.findAll('a')
                for a in links:
                    print baseurl + '' + a['href']
                    FH.writelines(baseurl + '' + a['href'])  # appending url  to baseurl to get ultimate link
                    FH.writelines('\n')
        AlterLInk(path, Dir)
        return 'Success'
    except Exception,e:
        print e
        return 'Failed'


try:
    Process("http://www.middlesexcountynj.gov/Government/Directory/Pages/directory.aspx", "county","Middlesex","Middlesex","county")

except Exception, e:
    print str(e)
    # contentWrap