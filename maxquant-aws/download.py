#!/bin/usr/env python2.7

import os
import sys
import tempfile
import atexit

#Global variables
TEMP_PATH = ''

#Functions
def cleanup():
    shutil.rmtree(TEMP_PATH)

#Create list of passed arguments
args = sys.argv[1:]

#If there are no arguements error exit code
if len(args) == 0:
    print "Error: No passed arguments."
    sys.exit(1)

#Create temp dir
TEMP_PATH =  tempfile.mkdtemp()
#os.mkdir("C:\Users\Administrator\Desktop\yoyoyo")
#TEMP_PATH = "C:\Users\Administrator\Desktop\yoyoyo" 

#Register cleanup
atexit.register(cleanup)

#Parse passed arguements and download to temp folder
while len(args) and len(args[0]) > 1:
    arg = args.pop(0)

    if os.path.isfile("C:\Users\Administrator\Box Sync\{}".format(arg)):
        print "Downloading {}...".format(arg)

        os.rename("C:\Users\Administrator\Box Sync\{}".format(arg), "{}\{}".format(TEMP_PATH,arg))
    
    else:
        print "Error: C:\Users\Administrator\Box Sync\{} does not exist".format(arg)


