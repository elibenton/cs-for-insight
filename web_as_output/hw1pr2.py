
# Eli Cohen
# Homework 1, Problem 2
# 8 February 2017
'''
EXTRA CREDIT ATTEMPT
The main of this file creates an letter_frequencies.html file automatically!


'''
import csv
from collections import defaultdict

#
# readcsv is a starting point - it returns the rows from a standard csv file...
#
def readcsv( csv_file_name ):
	try:
		csvfile = open( csv_file_name, newline='' ) 
		csvrows = csv.reader( csvfile )             

		all_rows = []                         
		for row in csvrows:                  
			all_rows.append( row )                

		del csvrows                     
		csvfile.close()                          
		return all_rows                        

	except FileNotFoundError as e:
		print("File not found: ", e)
		return []

#
#
#
def write_to_csv( first , second , third , filename ):
	try:
		
		list_of_rows = []
		lst = [first,second,third]

		for smaller_lst in lst:
			for elt in smaller_lst:
				list_of_rows.append(elt)
		
		csvfile = open( filename, "w", newline='' )
		filewriter = csv.writer( csvfile, delimiter=",")
		
		for row in list_of_rows:
			filewriter.writerow( row )
		csvfile.close()

	except:
		print("File", filename, "could not be opened for writing...")

#
# Returns distribution of first letter, weighted with word usage.
#
def Wcount_first():
	LoR = readcsv("wds.csv")
	counts = defaultdict(int)
	total = 0
	for Row in LoR:
		word = str(Row[0]).lower()     
		num  = float(Row[1])
		letter = word[0]
		counts[letter] += num
		total += num

	for l,f in counts.items():
		counts[l] = round(((f / total) * 100),2)

	first_lst = []
	for l,f in counts.items():
		first_lst.append([l,f])

	first_lst_ = sorted(first_lst)
	first_lst_.insert(0,["Frequencies Letters as First",""])	

	return first_lst_

#
# Returns the distribution of last letters, weighted with word usage.
#
def Wcount_last():
	LoR = readcsv("wds.csv")
	counts = defaultdict(int)
	total = 0
	for Row in LoR:
		word = str(Row[0]).lower()    
		num  = float(Row[1])
		letter = word[-1]
		counts[letter] += num
		total += num

	for l,f in counts.items():
		counts[l] = round(((f / total) * 100),2)

	last_lst = []
	for l,f in counts.items():
		last_lst.append([l,f])

	last_lst_ = sorted(last_lst)
	last_lst_.insert(0,["Frequencies Letters as Last",""])	

	return last_lst_

#
# Returns distribution of e's by where they appear in each wotd, weighted with word usage.
# 
def Wcount_e():
	LoR = readcsv("wds.csv")
	counts = defaultdict(int)
	total = 0
	for Row in LoR:
		word = str(Row[0]).lower()    
		num  = float(Row[1]) 
		
		for i in range(len(word)):
			if word[i] == "e":
				counts[i] += num
				total += num

	for l,f in counts.items():
		counts[l] = round(((f / total) * 100),2)

	e_lst = []
	for l,f in counts.items():
		e_lst.append([l,f])

	e_lst_ = sorted(e_lst)
	e_lst_.insert(0,["Frequencies of E's",""])	

	return e_lst_

#
# 
#
def csv_to_html_table( csvfilename ):
	
	data = readcsv(csvfilename)

	style_str ="<style> #table1 {color:black; margin:auto;} td {border: 1px solid rgb(200,200,200); padding: 15px;text-align: center;}</style>\n"

	html_str ="<!DOCTYPEhtml>\n<html>\n<head>\n<title>Letter Frequencies Website</title>\n"+style_str+"</head>\n<body>\n<table id = table1>\n"
	for i,row in enumerate(data):
		row_str = "<tr>\n"

		for j,col in enumerate(data[i]):
			val = data[i][j]
			row_str += "<td>"+str(val)+"</td>\n"

		row_str += "</td>"
		html_str += row_str

	html_str += "</tr>\n</table>\n</body>\n</html>"


	text_file = open("letter_frequencies.html", "w")
	text_file.write(html_str)
	text_file.close()

	return text_file

#
# main runs all fucntions.
#
def main():

	one = Wcount_first()
	two = Wcount_last()
	three = Wcount_e()

	write_to_csv(one,two,three,"frequencies.csv")
	csv_to_html_table( "frequencies.csv" )
		