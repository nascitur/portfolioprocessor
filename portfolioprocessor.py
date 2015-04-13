# portfolioprocessor.py 
#
# Goal of this is to process the XML output file exported from the
# Jira portfolio planner


def getthefile(default_filename):
	import mmap
	import os
	desktoppath = os.path.expanduser('~/Desktop/')
	user_filename = raw_input("Enter name of file (" + default_filename + "): ")
	if user_filename != '':
		default_filename = user_filename
	print "opening " + desktoppath + default_filename + "..."
	openfile = open(desktoppath + default_filename)
	stringified = mmap.mmap(openfile.fileno(), 0, access=mmap.ACCESS_READ)
	return stringified


def getthemelist(themestring):
	themestartpos = themestring.find('<themeCollection>')
	themeendpos = themestring.find('</themeCollection>')
	themestring = themestring[themestartpos:themeendpos]
	listindex = 0
	themelist = []
	while themestring.find('<title>') != -1:
		thisthemestart = themestring.find('<title>') + 16
		thisthemeend = themestring.find('</title>') - 3
		themelist.append(listindex)
		themelist[listindex] = themestring[thisthemestart:thisthemeend]
		print themelist[listindex]
		themestring = themestring[thisthemeend + 11:]
		listindex = listindex + 1
		print themestring.find('<title>')


filestring = getthefile('export.xml')
themelist = getthemelist(filestring)
print themelist