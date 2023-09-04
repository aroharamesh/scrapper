import urllib2
import os 
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
		

def Process():

	data_list=[]

	data= pdf_to_txt()
	d =data.split('which are listed on our site telephone directory.')[1]
	# print d.

	s= d.replace('\n', '').replace('\r', '').replace("Email",'').replace("2018",'|').replace("2020",'|').replace('-','')
	s= s.split("|")[:-1]
	print s



	for i in [s[0],s[2],s[3],s[-1]]:
		i= (i.strip()).split(' ')
		print i
		name = ' '.join(i[:-2])
		desi = i[-2]
		data_list.append([name,desi])
		print data_list	
	for i in data_list:
		print i
		print '-----'
Process()
# Process("http://www.metuchennj.org/metnj/GOVERNMENT/Borough%20Council/", "Council","Borough","Metuchen","Council",'18')
