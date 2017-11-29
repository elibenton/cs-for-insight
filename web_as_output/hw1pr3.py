#
# Eli Cohen
# Homework 1, Problem 3
# 8 February 2017
# 

'''
EXTRA CREDIT ATTEMPT
This program directly writes a file called obama.html! Check it out!

'''
import csv
from collections import defaultdict
import re

#
#
#
def readcsv( csv_file_name ):
	try:
		csvfile = open( csv_file_name, newline='' )
		csvrows = csv.reader( csvfile )

		counts = defaultdict(list)         
		for word,sub in csvrows:
			counts[word] = sub

		del csvrows                     
		csvfile.close()                           
		
		return counts                   

	except FileNotFoundError as e:
		print("File not found: ", e)
		return []


#
#
#
def annotate_text( text, annotations ):

	f = open(text)
	theText = f.readlines()

	style_string ="<style> p {} h1 {} </style>"
	header_string="<h1>Obama's Honest Farewell Address</h1>"
	new_html_string ="<!DOCTYPEhtml>\n<html>\n<head>\n<title>Obama's Real Goodbye</title>\n"+style_string+"</head>\n<body>"+header_string+"\n<p>"
	for line in theText:
		for word in re.split(r'(\s+)',line):
			if word in annotations:
				new_word = '<span style="color:{0};" title="{1}">{2}</span>'.format("blue", word, annotations[word])
			else:
				new_word = word

			new_html_string += new_word 

	footer_string="<h1>Obama's Real Farewell Address</h1>"
	new_html_string+="</p>\n"+footer_string+"</body>\n</html>"
	
	return new_html_string

#
#
#
def original_text( text, annotations ):

	f = open(text)
	theText = f.readlines()

	style_string ="<style> p {} h1 {} </style>"
	header_string="<h1>Obama's Actual Farewell Address</h1>"
	new_html_string ="\n<p>"
	for line in theText:
		for word in re.split(r'(\s+)',line):
			if word in annotations:
				new_word = '<span style="color:{0};">{1}</span>'.format("red",word)
			else:
				new_word = word

			new_html_string += new_word 

	new_html_string+="</p>\n</body>\n</html>"
	
	return new_html_string

#
# Just for testing
#
def main():

	dct = readcsv("slang.csv")
	new = annotate_text("obama.txt",dct)
	old = original_text("obama.txt",dct)

	text_file = open("obama.html", "w")
	text_file.write(new)
	text_file.write(old)
	
	text_file.close()

