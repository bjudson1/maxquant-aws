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

#----------Global variables----------------------
TEMP_PATH = ''
EXP_NAME = ''

#------------Functions--------------------------
def usage(status=0):
    print '''Usage: {} EXPERIMENT_NAME

        EXPERIMENT_NAME will also be the name of directory in box sync
    '''.format(os.path.basename(sys.argv[0])
    )
    sys.exit(status)

#question if needed since shut down vm
def cleanup():
    shutil.rmtree(TEMP_PATH)

 #----------Setup------------------------------
#Create temp dir
TEMP_PATH =  tempfile.mkdtemp()

#Register cleanup
atexit.register(cleanup)

#Create list of passed arguments
args = sys.argv[1:]

#trap if incorrect number of arguements passed
if len(args) != 1:
    print "Error01: Incorrect number of parameters."
    usage(1)

#get experiment name
EXP_NAME = args.pop(0)

#--------Start Box Sync----------------------------------------------
#os.system("C:\\Program\ File\\Box\\BoxSync\\BoxSync.exe")

boxsync = 'C:\\Program Files\\Box\\Box Sync\\BoxSync.exe'
subprocess.call([boxsync])

#--------Wait for Box Sync----------------------------------------------

#--------Interupt Box Sync----------------------------------------------
#find all running processes
process_data = subprocess.check_output("tasklist", shell=True)
#get the pid of boxsync.exe processes
pid = re.findall('BoxSync\.exe\s+([0-9]{3}|[0-9]{4}) RDP',process_data,flags=0)

if len(pid) == 0:
   print "Error: BoxSync.exe not found"

#Interupt all BoxSync.exe
for current_pid in pid:
    os.kill(int(current_pid), signal.SIGINT)

#------------Move Exp Dir to Temp Dir---------------------
if os.path.isdir("C:\Users\Administrator\Box Sync\{0}".format(EXP_NAME)):
    print "Downloading {} directory...".format(EXP_NAME)
    os.rename("C:\Users\Administrator\Box Sync\{0}".format(EXP_NAME),"{0}\{1}".format(TEMP_PATH,EXP_NAME))
else:
    print "Error02: experiment directory not found"
    sys.exit(2)
#-----------Read file_paths File-----------------------------------------
if os.path.isfile("{}\{}\\file_paths.txt".format(TEMP_PATH,EXP_NAME)):
    r = open("{}\{}\\file_paths.txt".format(TEMP_PATH,EXP_NAME),'r')
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

#-----------Edit XML----------------------
#open file w/ read write
xml_file = open("{}\{}\{}".format(TEMP_PATH,EXP_NAME,os.path.basename(xml_path[0])),'r+')


#for line in fileinput.input( "{}\{}\{}".format( TEMP_PATH,EXP_NAME,os.path.basename(xml_path[0]) ) ):
for line in xml_file.read():
	#update path of raw files
    for current_file_path in raw_file_paths:
        if "{}".format(current_file_path) in line :
            print "Updated {} in XML".format(os.path.basename(current_file_path))
        else:
            print "Failed to update in {} XML".format(os.path.basename(current_file_path))
        xml_file.write( line.replace("{}".format(current_file_path),"{}\{}".format(TEMP_PATH,os.path.basename(current_file_path))))

    #update path of .fasta file
    if "{}".format(fasta_path[0]) in line :
        print "Updated {} in XML".format(os.path.basename(fasta_path[0]))
    else:
        print "Failed to update in {} XML".format(os.path.basename(fasta_path[0]))

    xml_file.write( line.replace( "{}".format(fasta_path[0]), "{}\{}".format(TEMP_PATH,os.path.basename(fasta_path[0])) ) )

#close file
xml_file.close()
#-----------Run MaxQuant------------------
#os.system('C:\Users\Administrator\Desktop\MaxQuant_1.5.5.1\MaxQuant\MaxQuant.exe C:{0}\{1}'.format(TEMP_PATH,xml))

#maxquant = 'C:\\Users\\Administrator\\Desktop\\MaxQuant_1.5.5.1\\MaxQuant\\MaxQuant.exe C:{}\{}'.format(TEMP_PATH,xml)
#subprocess.call([maxquant])
# data trao for xml not in temp
print os.listdir('{}\{}'.format(TEMP_PATH,EXP_NAME))
if not os.path.isfile('{0}\{1}\{2}'.format(TEMP_PATH,EXP_NAME,xml[0])):
    print "Error03: xml not in temp dir"
    sys.exit(4)

print "Begin MaxQuant..."

file = 'C:\\Users\\Administrator\\Desktop\\MaxQuant_1.5.5.1\\MaxQuant\\bin\\MaxQuantCmd.exe {}\{}\{}'.format(TEMP_PATH,EXP_NAME,xml_path[0])
os.system('"' + file + '"')

#----------Wait till MaxQuant finishes----------------------------
process_data = subprocess.check_output("tasklist", shell=True)
running_maxs = re.findall('MaxQuant\.exe\s+([0-9]{3}|[0-9]{4}) RDP',process_data,flags=0)

#loop until no maquant.exe running
while len(running_maxs) != 0:
    process_data = subprocess.check_output("tasklist", shell=True)
    #get the pid of MaxQuant.exe processes
    running_maxs = re.findall('MaxQuant\.exe\s+([0-9]{3}|[0-9]{4}) RDP',process_data,flags=0)
    syxs.

#-------Upload Combined Folder-------------------------------------
#------Kill VM-----------------------------------------------------

 #instance = conn.get_only_instances(instance_ids=[instance_id])[0]
	# if instance.state == "running":
	#	print "Stopping instance %s" %  str(instance_id)
	#	instance.stop()


sys.exit(0)



