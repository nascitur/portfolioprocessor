# portfolioprocessor.py 
#
# Goal of this is to process the XML output file exported from the
# Jira portfolio planner


def getfile(default_filename):
	import mmap
	user_filename = input("Enter name of file (" + default_filename + "):");
	if user_filename != '':
		default_filename = user_filename
	openfile = open(default_filename)
	stringified = mmap.mmap(openfile.fileno(), 0, access=mmap.ACCESS_READ)
	return stringified


def getthemelist(themestring):
	themestartpos = themestring.find('<themeCollection>')
	themeendpos = themestring.find('</themeCollection>')
	themestring = themestring[themestartpos:themeendpos]
	listindex = 1
	themelist = []
	while themestring.find('<title>') != -1
		thisthemestart = themestring.find('<title>') + 16
		thisthemeend = themestring.find('</title>')
		themelist.append(listindex) = themestring[thisthemestart:thisthemeend]
		themestring = themestring[thisthemeend:]
		listindex = listindex + 1




filestring = getfile('~/Desktop/export.xml')
themelist = getthemelist(filestring)
print themelist