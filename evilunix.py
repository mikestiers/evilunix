import xattr
import os
import sys
import re
import pdb

logpath = os.getenv("HOME")+'/Desktop/log.txt'
logfile = open(logpath, 'w')
files = os.listdir('.')
modify = None

# check if user specified path
try:
	rootdir = sys.argv[1]
except:
	print "Specify a directory to scan. example: python2.7", sys.argv[0], "path_name"
	sys.exit()

# check if user has requested for modifiation to occur by finishing command with MODIFY argument
try:
	if sys.argv[2] == "MODIFY":
		modify = True
		print "Modifying files"
		print "Started"
		logfile.write("***MODIFYING " + rootdir + "***\n")
except:
	modify = False
	print "Files will not be modified.  To enable modification, type add 'MODIFY' to end of command"
	print "Started"
	logfile.write("***REPORTING ON: " + rootdir + "***\n")

def checkAttributes(filename):
	# try / except reading attributes because characters like colons and possibly other mac stuff cause exceptions
	try:
		attributes = xattr.listxattr(filename)
		# check if attributes exist, log it
		if not (attributes):
			logfile.write("FAIL: HAS NO ATTRIBUTES: " + filename + "\n")
			checkFileSize(filename + "HAS NO ATTRIBUTES")
		for attribute in attributes:
			if attribute == "com.apple.FinderInfo":
				# file is assumed to be ok
				break
			else:
				logfile.write("FAIL: MISSING FINDER ATTR: " + filename + "\n")
				if attribute == "com.apple.ResourceFork":
					# check for file size.  if it is zero and has a resource fork, it needs to be repaired
					checkFileSize(filename, "HAS RESOURCE FORK")
					resource = xattr.getxattr(filename,'com.apple.ResourceFork')
					if "PS-Adobe" in str(resource):
						changePostScript(filename)
					elif "PICT" in str(resource):
						changeQuark(filename)
					else:
						changeSuitcase(filename)
	except:
		#logfile.write("FAIL: Exception reading attributes: " + filename + "\n")
		pass

def doNothing():
	pass

def checkFileSize(filename, reason):
	try:
		#pdb.set.trace()
		filestats = os.stat(filename)
		if (filestats.st_size == 0):
			logfile.write("FAIL: SIZE ZERO: " + reason + ": " + filename + "\n")
			# do something.  we have not decided how to handle these yet.
		#else:
		#	logfile.write("PASS: NOT ZERO: " + reason + ": " + filename + "\n")
	except:
		logfile.write("FAIL: Exception reading file stats: " + filename + "\n")

def checkFilenameLength(filename):
	try:
		if (filename.__len__() >= 240):
			logfile.write("FAIL: FILENAME TOO LONG: " + filename + "\n")
	except:
		logfile.write("FAIL: Exception reading filename length\n")

def changePostScript(filename):
	logfile.write("CHANGE POST SCRIPT: " + filename + "\n")
	if (modify == True):
		command = "xattr -wx com.apple.FinderInfo '4C 57 46 4E 41 53 50 46 20 00 FF FF FF FF 00 00 00 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00' " + "'" + filename + "'"
		try:
			logfile.write("MODIFYING: " + filename + "\n")
			os.system(command)
		except:
			logfile.write("FAIL: Exception unable to modify" + fileanme + "\n")

def changeSuitcase(filename):
	logfile.write("CHANGE SUITCASE: " + filename + "\n")
	if (modify == True):
		command = "xattr -wx com.apple.FinderInfo '46 46 49 4C 44 4D 4F 56 00 00 FF FF FF FF 00 00 00 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00' " + "'" + filename + "'"
		try:
			logfile.write("MODIFYING: " + filename + "\n")
			os.system(command)
		except:
			logfile.write("FAIL: Exception unable to modify" + fileanme + "\n")

def changeT1(filename):
	pass #marking this as a pass because we cannot determine if T1s need anything yet

def changeQuark(filename):
	# logging a quark file, but not making any changes because we cannot determine if there are any bad quark files
	logfile.write("CHANGE QUARK FILE: " + filename + "\n")

# run through the file system
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		fs = str(file)
		filename = os.path.join(subdir, file)
		# check for specific extensions and existence of extension, otherwise it has no extension and should be processsed
		if (".t1" in fs):
			changeT1(filename)
		elif ("." in fs):
			checkFilenameLength(filename)
		else:
			checkAttributes(filename)
			checkFilenameLength(filename)

print "Finished"
logfile.close()
