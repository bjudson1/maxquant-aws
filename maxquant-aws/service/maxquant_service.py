#!/usr/bin/env python

import os
import sys
import re
import tempfile
import atexit
import shutil
import subprocess
import signal
import fileinput
import time
import boto.ec2

#----------Global variables----------------------
TEMP_PATH = ''
EXP_NAME = ''
FROM = "MaxQuant"
EMAIL_TO_SEND_TO = "brenden.judson@gmail.com"
SUBJECT = "hi"
TEXT = email_message
EMAIL_TEXT = "Your MaxQuant test {} has failed to complete."

#------------Functions--------------------------
def usage(status=0):
    print '''Usage: {} EXPERIMENT_NAME

        EXPERIMENT_NAME will also be the name of directory in box sync
    '''.format(os.path.basename(sys.argv[0])
    )
    sys.exit(status)

#question if needed since shut down vm
def cleanup():
    #-------Send Email-------------------------------------------------

    message = """\
    From: MaxQuant
    To: %s
    Subject: MaxQuant Update

    %s
    """ % (", ".join(EMAIL_TO_SEND_TO), TEXT)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login("brenden.judson@gmail.com", getpass.getpass())
    server.sendmail("brenden.judson@gmail.com", EMAIL_TO_SEND_TO, message)
    server.quit()

    shutil.rmtree(TEMP_PATH)

    #instance = conn.get_only_instances(instance_ids=[instance_id])[0]
	# if instance.state == "running":
	#	print "Stopping instance %s" %  str(instance_id)
	#	instance.stop()

 #----------Setup------------------------------
#Create temp dir
TEMP_PATH =  tempfile.mkdtemp()

#Register cleanup
#atexit.register(cleanup)

#Create list of passed arguments
#args = sys.argv[1:]

#trap if incorrect number of arguements passed
#if len(args) != 1:
 #   print "Error01: Incorrect number of parameters."
 #   usage(1)

#get experiment name
#EXP_NAME = args.pop(0)

try:
    ## Get connection to aws EC2.	
    conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id='aws_access_key_id',aws_secret_access_key='aws_secret_access_key')

#Catch failed connection
except Exception, ec:
    error = " %s " % str(ec)
    print error
    sys.exit(5)

command = 'powershell (Invoke-WebRequest -Uri http://169.254.169.254/latest/meta-data/instance-id).Content'
instance_id = subprocess.check_output('"' + command + '"', shell=True).strip()

tags = conn.get_only_instances(instance_ids=[instance_id])[0].tags["Experiment-Name"]
#os.system('"' + command + '"')
EXP_NAME = tags

#--------Start Box Sync----------------------------------------------
#os.system("C:\\Program\ File\\Box\\BoxSync\\BoxSync.exe")

#boxsync = 'C:\\Program Files\\Box\\Box Sync\\BoxSync.exe'
#subprocess.call([boxsync])

#--------Wait for Box Sync----------------------------------------------
while not os.path.isfile("C:\Users\Administrator\Box Sync\{0}\\file_paths.txt".format(EXP_NAME)):
    time.sleep(5)

#--------Interupt Box Sync----------------------------------------------
#find all running processes
#process_data = subprocess.check_output("tasklist", shell=True)
#get the pid of boxsync.exe processes
#pid = re.findall('BoxSync\.exe\s+([0-9]{3}|[0-9]{4}) RDP',process_data,flags=0)

#if len(pid) == 0:
#   print "Error: BoxSync.exe not found"

#Interupt all BoxSync.exe
#for current_pid in pid:
 #   os.kill(int(current_pid), signal.SIGINT)
#-----------Read file_paths File-----------------------------------------
if os.path.isfile("C:\Users\Administrator\Box Sync\{0}\\file_paths.txt".format(EXP_NAME)):
    r = open("C:\Users\Administrator\Box Sync\{0}\\file_paths.txt".format(EXP_NAME),'r')
    file_paths_data = r.read()

    raw_file_paths = re.findall('.+\.raw',file_paths_data,flags=0)
    if len(raw_file_paths) == 0:
        print "Error03: .raw files not found in file_paths.txt"
        sys.exit(3)
    xml_path = re.findall('.+\.xml',file_paths_data,flags=0)
    if len(xml_path) == 0:
        print "Error03: .xml file not found in file_paths.txt"
        sys.exit(3)
    fasta_path = re.findall('.+\.fasta',file_paths_data,flags=0)
    if len(fasta_path) == 0:
        print "Error03: .fasta file not found in file_paths.txt"
        sys.exit(3)
        

else:
	print "Error03: file_paths.txt not found"
	sys.exit(3)

#close file_paths file
r.close()

#--------Wait for Box Sync----------------------------------------------
while not os.path.isfile("C:\Users\Administrator\Box Sync\{}\{}".format(EXP_NAME,os.path.basename(xml_path[0]))):
    time.sleep(5)
while not os.path.isfile("C:\Users\Administrator\Box Sync\{}\{}".format(EXP_NAME,os.path.basename(fasta_path[0]))):
    time.sleep(5)
for current_file in raw_file_paths:
    while not os.path.isfile("C:\Users\Administrator\Box Sync\{}\{}".format(EXP_NAME,os.path.basename(current_file))):
        time.sleep(5)

#------------Move Exp Dir to Temp Dir---------------------
if os.path.isdir("C:\Users\Administrator\Box Sync\{0}".format(EXP_NAME)):
    print "Downloading {} directory...".format(EXP_NAME)
    os.rename("C:\Users\Administrator\Box Sync\{0}".format(EXP_NAME),"{0}\{1}".format(TEMP_PATH,EXP_NAME))
else:
    print "Error02: experiment directory not found"
    sys.exit(2)

#-----------Edit XML----------------------
#open file w/ read write
xml_file = open("{}\{}\{}".format(TEMP_PATH,EXP_NAME,os.path.basename(xml_path[0])),'r+')

text = ""

for line in xml_file:
   
    for current_file_path in raw_file_paths:
         line = line.replace("{}".format(current_file_path),"{}\{}\{}".format(TEMP_PATH,EXP_NAME,os.path.basename(current_file_path)))

    line = line.replace("{}".format(fasta_path[0]),"{}\{}\{}".format(TEMP_PATH,EXP_NAME,os.path.basename(fasta_path[0])))
    text += line
    
xml_file.seek(0)
xml_file.write(text)
xml_file.truncate()
xml_file.close()

#-----------Run MaxQuant------------------
# data trao for xml not in temp
if not os.path.isfile('{0}\{1}\{2}'.format(TEMP_PATH,EXP_NAME,os.path.basename(xml_path[0]))):
    print "Error03: xml not in temp dir"
    sys.exit(4)

print "Begin MaxQuant..."

maxquant = 'C:\\Users\\Administrator\\Desktop\\MaxQuant_1.5.5.1\\MaxQuant\\bin\\MaxQuantCmd.exe {}\{}\{}'.format(TEMP_PATH,EXP_NAME,os.path.basename(xml_path[0]))
os.system('"' + maxquant + '"')

#----------Wait till MaxQuant finishes----------------------------
process_data = subprocess.check_output("tasklist", shell=True)
running_maxs = re.findall('MaxQuant\.exe\s+([0-9]{3}|[0-9]{4}) RDP',process_data,flags=0)

#loop until no maquant.exe running
while len(running_maxs) != 0:
    process_data = subprocess.check_output("tasklist", shell=True)
    #get the pid of MaxQuant.exe processes
    running_maxs = re.findall('MaxQuant\.exe\s+([0-9]{3}|[0-9]{4}) RDP',process_data,flags=0)
    time.sleep(60)

#-------Upload Combined Folder-------------------------------------
os.mkdir("C:\Users\Administrator\Box Sync\{}_output".format(EXP_NAME))

if os.path.isdir('{0}\{1}\combined'.format(TEMP_PATH,EXP_NAME)):
    os.rename('{0}\{1}\combined'.format(TEMP_PATH,EXP_NAME),"C:\Users\Administrator\Box Sync\{}_output\combined".format(EXP_NAME))
else:
    print "Error03: could not find combined folder"   

EMAIL_TEXT = "Your MaxQuant test {} has successfuly completed."
 
sys.exit(0)



