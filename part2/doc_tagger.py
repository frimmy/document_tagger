import re
import sys
from pg_sample_texts import DIV_COMM, MAG_CART
from argparse import ArgumentParser #import the ArgumentParser object from this module, allows for more than one argument into command line
import os


argparser = ArgumentParser() #creates a parser object


argparser.add_argument('--search','-s', dest='search',
                      nargs='+', help='a string for the parser to search for')
argparser.add_argument('-d', '--dir',
                        dest='directory', help='string for directory to search text terms')

arguments = argparser.parse_args() #unpacks the arguments entered on the command line

terms = arguments.search #stores search terms into variable t 
directory = arguments.directory

documents = [DIV_COMM, MAG_CART] #for testing regex in proj gut pt 1

# first we need to do something with the user supplied keywords
# which we're getting with sys.argv. Remember, the script name itself
# is at index 0 in sys.argv, so we'll slice everything from index 1 forward.
searches = {}
for kw in terms:
  searches[kw] = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)

# PREPARE OUR REGEXES FOR METADATA SEARCHES #
# we'll use re.compile() here, which allows you to assign a regex pattern
# to a variable. We'll do this for each our metadata fields.
# 
# Also note how we're using paretheses to create two search groups. Looking
# at title_search, see how we use one group to match on the presence of "title:".
# 
# Also, note how in the second group is a named group -- we use ?p<name> .
# 
# Finally, note that we're passing the re.IGNORECASE flag as an optional
# argument to re.compile. We're doing this because it's human beings who create
# the metadata headers at the top of Project gutenberg docs, and we want to account 
# for possibility of "title: Some Title", "Title: Some Title", and "TITLE: Some Title").
title_search = re.compile(r'(title:\s*)(?P<title>.*(\n.*\S)*)', re.IGNORECASE)
author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)
illustrator_search = re.compile(r'(illustrator:)(?P<illustrator>.*)', re.IGNORECASE)

# now iterate over the documents and extract and print output about metadata
# for each one. Note the use of enumerate here, which gives you a counter variable
# (in this case 'i') that keeps track of the index of the list (in this case documents)
# your currently on in your loop. You should memorize how enumerate works, and google it
# if you need more explanation. It's a highly productive built in function, and there are
# common problems that you'll encounter as a programmer that enumerate is great for.
for i, doc in enumerate(os.listdir(directory)):
  
  if doc.endswith('.txt'):

    print "Processing file {0}".format(i + 1)

    doc_path = os.path.join(directory, doc)

    with open(doc_path, 'r') as d:
      full_text = d.read()

    title = re.search(title_search, full_text).group('title')
    author = re.search(author_search, full_text)
    translator = re.search(translator_search, full_text)
    illustrator = re.search(illustrator_search, full_text)
    if author: 
      author = author.group('author')
    if translator:
      translator = translator.group('translator')
    if illustrator:
      illustrator = illustrator.group('illustrator')
    print "***" * 25
    print "Here's the info for file {}:".format(doc)
    print "Title:  {}".format(title)
    print "Author(s): {}".format(author)
    print "Translator(s): {}".format(translator)
    print "Illustrator(s): {}".format(illustrator)
    print "***" * 25
    print "Here's the keyword info for file {}:".format(doc)
    
    for search in searches:
      print "\"{0}\": {1}".format(search, len(re.findall(searches[search], full_text)))

    print "\n"