import os
for root, dirs, files in os.walk("./Council", topdown=False):
   a=0
   for name in files:
   	with open(os.path.join(root, name),'r') as r:
   		d = r.readlines()
   		a=a+len(d)
   	print a


