import re
import sys
from argparse import ArgumentParser #import the ArgumentParser object from this module, allows for more than one argument into command line
import os

def parse_for_terms_and_dir():
	argparser = ArgumentParser() #creates a parser object
	argparser.add_argument('--search','-s', dest='search',
	                      nargs='+', help='a string for the parser to search for')
	argparser.add_argument('-d', '--dir',
	                        dest='directory', help='string for directory to search text terms')
	arguments = argparser.parse_args() #unpacks the arguments entered on the command line
	terms = arguments.search #stores search terms into variable t 
	directory = arguments.directory

	return {"terms":terms,"directory":directory}

#Iterating over and opening files

def files_in_dir(directory, terms, metadata):
	for i,doc in enumerate(os.listdir(directory)):
		if doc.endswith('.txt'):
			print "Processing file {}".format(i+1)
			doc_path = os.path.join(directory, doc)
			with open(doc_path, 'r') as d:
				full_text = d.read()
			# compile regex searches for metadata and search terms
			search_terms_and_metadata = compiled_search(terms, metadata)
			# print meta
			print "***" * 25
			print_metadata(search_doc(search_terms_and_metadata["metasearch"], full_text), doc, metadata)
			print "***" * 25
			# print term search
			count_search_words(search_terms_and_metadata["searches"], full_text)
			print "\n"
			

def search_doc(metasearch, full_text):
	metaresults = {}
	for i,j in metasearch.items():
		if re.search(j, full_text):
			metaresults[i] = re.search(j, full_text).group(i)
		else:
			metaresults[i] = re.search(j, full_text)
	return metaresults

# Compiling user supplied keywords into  regular expressions
def compiled_search(terms, metadata):
	searches = {}
	for kw in terms:
		searches[kw] = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)
	metasearch = {}	
	for i in metadata:
		metasearch[i] = re.compile(r'({0}:)(?P<{0}>.*)'.format(i), re.IGNORECASE)
	return {"searches":searches, "metasearch": metasearch}

# Counting keywords in a document
def count_search_words(searches, full_text):
	for search in searches:
	  print "\"{0}\": {1}".format(search, len(re.findall(searches[search], full_text)))
	print "\n"

def print_metadata(metaresults, doc, metadata):
	print "Here's the info for file {}:".format(doc)
	for i in metadata:
		print i.capitalize(),":",metaresults[i]

def main():
	terms_and_dir = parse_for_terms_and_dir()
	metadata = ['title','author', 'translator','illustrator']
	files_in_dir(terms_and_dir["directory"], terms_and_dir["terms"], metadata)
	
if __name__ == '__main__':
      main()
      