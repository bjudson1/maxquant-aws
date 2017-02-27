#!/bin/usr/env python2.7

import os
import sys

args = sys.argv[1:]

#pass files to upload as arguements to script 

if len(args) == 0:
    print "Error: No passed arguments."
    sys.exit(1)

while len(args) and len(args[0]) > 1:
    arg = args.pop(0)
    
    if os.path.isfile("C:\Users\Administrator\Desktop\upload\{}".format(arg)):
        print "Uploading {}...".format(arg)
   
        os.rename("C:\Users\Administrator\Desktop\upload\{}".format(arg), "C:\Users\Administrator\Box Sync\{}".format(arg)) 
    else:
         print "Error: C:\Users\Administrator\Box Sync\{} does not exist".format(arg)

sys.exit(0)
