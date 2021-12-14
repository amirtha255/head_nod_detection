import sys
import os
import re
import csv
import pandas as pd

import xml.etree.ElementTree as ET

"""
Prerequisite - dataset_cardiff.csv created from create_dataset.py
"""

nod_counter = 0
other_counter = 0


file_open='C:\\Users\\amirtha\\Desktop\\special_problems\\dataset_cardiff.csv' #just to get headings
file_open = open(file_open,'r')

lines = file_open.readlines()
line_1 = lines[0]


len_rows = len(lines)

print('Number of samples is ',len_rows)


df = pd.read_csv('C:\\Users\\amirtha\\Desktop\\special_problems\\dataset_cardiff.csv')
columns=df.columns.tolist()



file_other = 'C:\\Users\\amirtha\\Desktop\\special_problems\\Self-Disclosure-Head-Motion-Detection-master\\Self-Disclosure-Head-Motion-Detection-master\\data\\other\\other_{}.csv'.format(other_counter)
file_other=open(file_other, 'w',newline='')
csvwriter_other = csv.writer(file_other)
csvwriter_other.writerow(columns)
line_count_other = 0
i=1
while i<len_rows:

	fields = lines[i].strip().split(',')
	nod_value = int(fields[-1])

	fields_textfile = fields[-2]
	fields = fields[:-2]
	fields = [float(f) for f in fields]
	fields.append(fields_textfile)

	if nod_value==1:
		

		print('IN NOD')

		file_csv='C:\\Users\\amirtha\\Desktop\\special_problems\\Self-Disclosure-Head-Motion-Detection-master\\Self-Disclosure-Head-Motion-Detection-master\\data\\nod\\nod_{}.csv'.format(nod_counter)
		# writing to csv file 
		csvfile=open(file_csv, 'w',newline='')  
		    # creating a csv writer object 
		csvwriter = csv.writer(csvfile) 
		#csvwriter.writerow(line_1)       TODO
		    # writing the fields 
		k=0

		while nod_value == 1 and i<len_rows:

			if k==0:
				csvwriter.writerow(columns)
			k+=1
			csvwriter.writerow(fields) 
			i+=1
			fields = lines[i].strip().split(',')

			nod_value = int(fields[-1])
			fields_textfile = fields[-2]
			fields = fields[:-2]
			fields = [float(f) for f in fields]
			fields.append(fields_textfile)

		#while nod_value==1:
		

		nod_counter+=1

		other_counter+=1


		nod_value=0
		i+=1


		file_other.close()
		csvfile.close()

		file_other = 'C:\\Users\\amirtha\\Desktop\\special_problems\\Self-Disclosure-Head-Motion-Detection-master\\Self-Disclosure-Head-Motion-Detection-master\\data\\other\\other_{}.csv'.format(other_counter)
		file_other=open(file_other, 'w',newline='')
		csvwriter_other = csv.writer(file_other)
		csvwriter_other.writerow(columns)
		line_count_other=0


		#i-=1

	else:

		

		csvwriter_other.writerow(fields) 
		line_count_other +=1

		if line_count_other > 2100:
			
			file_other = 'C:\\Users\\amirtha\\Desktop\\special_problems\\Self-Disclosure-Head-Motion-Detection-master\\Self-Disclosure-Head-Motion-Detection-master\\data\\other\\other_{}.csv'.format(other_counter)
			file_other=open(file_other, 'w',newline='')
			csvwriter_other = csv.writer(file_other)
			csvwriter_other.writerow(columns)
			line_count_other=0
			#other_counter+=1

		i+=1


print('Number OF NODS IS ',nod_counter)
print('Number OF OTHERS IS ',other_counter)

