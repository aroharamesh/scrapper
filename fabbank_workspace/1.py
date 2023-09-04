# #IMPORTS STARTS HERE
# import json
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# import re
# import time
# import pandas as pd
# #imports ends here

# import random

# def level_1(q_p):#Function 


# 	url="https://www.google.com/"
# 	desc = {} 
# 	url=str(url)
# 	chrome_path = r"C:\\iamhere\\chromedriver.exe"
# 	driver = webdriver.Chrome(chrome_path)
# 	driver.get(url)
# 	elem = driver.find_element_by_name("q")
# 	elem.send_keys(str(q_p))
# 	elem.submit()

# 	try:
		

# 		full_div= (driver.find_element_by_class_name('xpdopen'))
# 		# website = full_div.find_element_by_class_name('ab_button').get_attribute("href")
# 		# print (website)
# 		try:
# 			Website= (full_div.find_element_by_link_text("Website").get_attribute("href"))
# 			# print (Website)
			
# 		except Exception as e:
# 			Website = ""

# 		try:
# 			Directions= (full_div.find_element_by_link_text("Directions").get_attribute("href"))
# 		except Exception as e:
# 			Directions = ""
		
# 		# print (Directions)


# 		try:
# 			rating=(full_div.find_element_by_class_name('Ob2kfd').text).replace('\n', ' ').replace('\r', '')
# 			# print (rating)
			

# 		except Exception as e:
# 			rating = ''

# 		try:
# 			name =(full_div.find_element_by_class_name('kno-ecr-pt').text)
# 			# print (name)
# 			# print ('name')


# 		except Exception as e:
# 			name = ''
# 			# print (str(e))
     
# 		try:
# 			Address =(full_div.find_element_by_class_name('i4J0ge').text).replace('\n', ' ').replace('\r', '')
# 			# print (Address.split('Phone:')[0])
# 			Addressline = (Address.split('Phone:')[0])
# 			# print ("Phone: "+Address.split('Phone:')[1])
# 			phoneline = ("Phone: "+Address.split('Phone:')[1])

# 		except Exception as e:
# 			Addressline = ''
# 			phoneline = ''


# 		driver.close()

# 		return {"input": q_p, "name": name, "Address": Addressline, "Phone": phoneline, "Rating": rating, "Website_url": Website, "Directions_url": Directions, "status":1}

# 	except Exception as e:
# 		driver.close()
# 		return {"input": q_p, "name": '', "Address": '', "Phone": '', "Rating": '', "Website_url": '', "Directions_url": '', "status":0}
# 		# pass

# import pandas as pd
# import re
# import csv 

# url="https://www.google.com/"

# df = pd.read_csv('./data/sample_merchants_subset.csv', nrows=400)
# df = df[250:300]
# # print (df["Merchant Transaction Free Text"])
out_put_file = "./output/level_1.csv"



# for query in (df["Merchant Transaction Free Text"]):
# 	q_p = re.sub('\\s+',' ', ( re.sub('[^a-zA-Z0-9 \n\\.]', '', (re.sub('\\s+',' ', query))) ))
# 	# print (q_p)
# 	out_dict=level_1(q_p)
# 	print (list(out_dict.values()))


# 	with open(out_put_file, 'a', encoding='utf-8') as csvFile:
# 	    writer = csv.writer(csvFile)
# 	    writer.writerow((list(out_dict.values())))

# 	csvFile.close()




import pandas as pd 
df = pd.read_csv(out_put_file)
print ((df).summary())
# print (df["Phone"].isnull().sum())