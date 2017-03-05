#!/usr/bin/env python

import os
import sys
import re
import subprocess
import signal
import boto.ec2

#----------Global Variable------------------------------------
EXP_NAME = ''


#----------Functions-------------------------------------------
#display usage and exit with passed status
def usage(status=0):
    print '''Usage: {} C:\\foo.xml EXPERIMENT_NAME
  
          EXPERIMENT_NAME will also be the name of directory in box sync
    '''.format(os.path.basename(sys.argv[0])
    )
    sys.exit(status)


#----Get Passed Arguements--------------------------------------
args = sys.argv[1:]

#trap if incorrect number of arguements passed
if len(args) != 2:
    print "Error: Incorrect number of parameters."
    usage(1)

#parse through arguements
#while len(args) and len(args[0]) > 1:
xml = args.pop(0)
EXP_NAME = args.pop(0)
 
#--------Interupt Box Sync----------------------------------------------
#find all running processes
#process_data = subprocess.check_output("tasklist", shell=True)
#get the pid of boxsync.exe processes
#pid = re.findall('BoxSync\.exe\s+([0-9]{3}|[0-9]{4}) RDP',process_data,flags=0)

#if len(pid) == 0:
 #   print "Error: BoxSync.exe not found"

#Interupt all BoxSync.exe
#for current_pid in pid:
  #  os.kill(int(current_pid), signal.SIGINT)

#---------Get Info from xml-------------------------------------------
    
#if xml exists open and get raw files also # threads
if os.path.isfile("{}".format(xml)):
    r = open(xml,'r')
    data = r.read()
    raw_files = re.findall('>(.+raw)',data,flags=0)
    fasta = re.findall('>(.+fasta)',data,flags=0)
    threads = re.findall('numThreads>([0-9]{1}|[0-9]{2})',data,flags=0)

else:
    print "Error: {} does not exist".format(xml)
    sys.exit(2)

#create directory in box sync
os.mkdir("C:\Users\Administrator\Box Sync\{}".format(EXP_NAME))

#close file
r.close()

#---------Create file_paths.txt-----------------------------------------------
file_paths = open("file_paths.txt","w+")
text = ""
text += xml + '\n'
text += fasta[0] + '\n'
for current_file in raw_files:
    text += current_file + '\n'

file_paths.write(text)
file_paths.close()

#---------Upload Files to Box Sync-------------------------------------------
#move file_paths file
print "Uploading file_paths.txt..."
os.rename(".\\file_paths.txt", "C:\Users\Administrator\Box Sync\{0}\\file_paths.txt".format(EXP_NAME))  

#move xml to box sync folder (upload)
print "Uploading {}...".format(xml)
os.rename("{}".format(xml), "C:\Users\Administrator\Box Sync\{0}\{1}".format(EXP_NAME,os.path.basename(xml)))  

#move xml to box sync folder (upload)
print "Uploading {}...".format(fasta[0])
os.rename("{}".format(fasta[0]), "C:\Users\Administrator\Box Sync\{0}\{1}".format(EXP_NAME,os.path.basename(fasta[0])))  

#loop through all found raw files
for current_file in raw_files:
    #if the raw file exists, move to box sync folder (upload)
    if os.path.isfile("{}".format(current_file)):
        print "Uploading {}...".format(current_file)
        os.rename("{}".format(current_file), "C:\Users\Administrator\Box Sync\{0}\{1}".format(EXP_NAME,os.path.basename(current_file))) 
    #else file doesnt exist reprot error and exit code
    else:
        print "Error: {} does not exist".format(current_file)
        sys.exit(2)
#-------------Run Box Sync--------------------------------------------------
#os.system("C:\\Program File\\Box\\BoxSync\\BoxSync.exe")
#os.system("C:\Program File\Box\BoxSync\BoxSync.exe")

#-------------Wait for Sync--------------------------------------------------

#-------------Create EC2 Instance-------------------------------------------

#make connection to region


#choose instance type based on number of threads handling maxquant
# threads <= vCPUs
# max = 16 vCPU
if int(threads[0]) <= 2:
	my_instance_type = 'c4.large'
elif int(threads[0]) <= 4:
	my_instance_type = 'c4.xlarge'
elif int(threads[0]) <= 8:
	my_instance_type = 'c4.2xlarge'
else:
	my_instance_type = 'c4.4xlarge'

#Connect to region
try:
    ## Get connection to aws EC2.	
    conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id='aws_access_key_id',aws_secret_access_key='aws_secret_access_key')

#Catch failed connection
except Exception, ec:
    error = " %s " % str(ec)
    print error
    sys.exit(5)

#Create instance
try:
    reservation = conn.run_instances(
    'ami-9dfb76fd',
    key_name = 'brendenAWSchem',
    instance_type = my_instance_type,
    security_groups = ['launch-wizard-4'])

    for instance in reservation.instances:
    	instance.add_tag("Experiment-Name", EXP_NAME)

#Catch failed creation
except Exception, ec:
    error = " %s " % str(ec)
    print error
    sys.exit(5)

sys.exit(0)
