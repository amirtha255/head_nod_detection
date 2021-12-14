import sys
import os
import re
import csv
import pandas as pd

import xml.etree.ElementTree as ET

"""

Run this script from base directory of cardiff dataset so the script could recursively find the files.
Outputs dataset_cardiff.csv

"""




total_nods=0

def parseXML(xmlfile,nod_start_time_list,nod_end_time_list):
  
	# create element tree object
	tree = ET.parse(xmlfile)
  
	# get root element
	root = tree.getroot()


	for child in root:

		if child.tag=='TIER' :
			if child.attrib['TIER_ID']=='Head Nodding':
				
				for item in child:
					if item.tag=='ANNOTATION':

						for last_level in item:

							nod_start_time_list.append(last_level.attrib['TIME_SLOT_REF1'])
							nod_end_time_list.append(last_level.attrib['TIME_SLOT_REF2'])


	#once we get nod_time_list appended , substitue actual values
	for child in root:
		if child.tag=='TIME_ORDER':

			for item in child:
					if item.attrib['TIME_SLOT_ID'] in nod_start_time_list:
						#print(item.attrib['TIME_VALUE'])
						#print(item.attrib['TIME_SLOT_ID'])

						nod_start_time_list[nod_start_time_list.index( item.attrib['TIME_SLOT_ID'] )] = float(item.attrib['TIME_VALUE'])/1000 # 1000 before or after ????

					elif item.attrib['TIME_SLOT_ID'] in nod_end_time_list:
						#print(item.attrib['TIME_VALUE'])
						#print(item.attrib['TIME_SLOT_ID'])	

						nod_end_time_list[nod_end_time_list.index( item.attrib['TIME_SLOT_ID'] )] = float(item.attrib['TIME_VALUE'])/1000	

top = os.getcwd()

top = top+'\\cardiff' #\\P3_P4_1502\\P3_P4_1502\\P3_P4_1502_C1'  # change to only cardif todo


file_open='C:\\Users\\amirtha\\Desktop\\special_problems\\cardiff\\P3_P4_1502\\P3_P4_1502\\P3_P4_1502_C1\\P3_P4_1502_C1.txt' #just to get headings
file1 = open(file_open,'r')

fields = file1.readlines()
fields=fields[0]

fields = fields.strip().split(',')  #adding first row to cardiff

#todo string to int ?????
fields.append('video_name')
fields.append('nod')

# name of csv file 
filename = "dataset_cardiff.csv"
    
# writing to csv file 
csvfile=open(filename, 'w',newline='')  
    # creating a csv writer object 
csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
csvwriter.writerow(fields) 



# create 3 new folders for training nod,others.


line_count = 0



for root, dirs, files in os.walk(top, topdown=False):

	if re.search('C',os.path.basename(root)):
		
		basename=os.path.basename(root)


		nod_start_time_list = []
		nod_end_time_list = []
		eav_file=''
		ann_file=''


		for file in files:

			print(nod_start_time_list,nod_start_time_list)

			file_basename= file.split('.')[0]
			file_ext = file.split('.')[1]




			if file_basename==basename and file_ext=='eaf':
				eav_file=os.path.join(root,file)
				print(eav_file)
				parseXML(eav_file,nod_start_time_list,nod_end_time_list)
				total_nods+=len(nod_start_time_list)

			if file_basename==basename and file_ext=='txt':
				ann_file=os.path.join(root,file)
				print(ann_file)
			

			#create dictionary and check if the frame time overlaps a nod interval then mark nod as one
			
		i=0
		n=len(nod_start_time_list)


		if ann_file!='':
				try:
					file1 = open(ann_file, 'r')
					Lines = file1.readlines()[1:]
					 
					count = 0
					# Strips the newline character
					for line in Lines:

						line_text = line.strip().split(',')

						line_text = [float(l) for l in line_text]

						line_text.append(basename)

						frame_time = (line_text[1]) #checkkkkkk

						if frame_time>=nod_start_time_list[i] and frame_time<=nod_end_time_list[i]:
							line_text.append(1)
							print('nod detected',frame_time,nod_start_time_list[i], nod_end_time_list[i])

						elif frame_time<=nod_start_time_list[i] and frame_time<=nod_end_time_list[i]:


							if i<n-1:
								i+=1
							line_text.append(0)


						else:
							line_text.append(0)  # for nod
						


						csvwriter.writerow(line_text)



				except Exception as err:
					print(err)
			




print('Total nods is ',total_nods)