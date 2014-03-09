import sys
import os

directory = sys.argv[1]

for fl in (os.listdir(directory)):  #for each item that appears in the directory
    if fl.endswith('.txt'):       #if it's a text file
        print 'Processing {0}.'.format(fl)

        fl_path = os.path.join(directory, fl) #the full path to the file is the directory plus
                                              #the file name

        with open(fl_path, 'r') as f:         #open the file as f
            full_text = f.read()              #assign its contents to the var full_text

        print '{0} is {1} characters long\n\n'.format(fl, len(full_text))