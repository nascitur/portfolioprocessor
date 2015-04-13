# portfolioprocessor.py 
#
# Goal of this is to process the XML output file exported from the
# Jira portfolio planner

# Import necessary modules

import mmap
import os

# getthefile()
# takes a default filename as the input and requests user input
# hardcoded to look on the mac desktop
# returns an mmap string of the file

def getthefile(default_filename):
	desktoppath = os.path.expanduser('~/Desktop/')
	user_filename = raw_input("Enter name of file (" + default_filename + "): ")
	if user_filename != '':
		default_filename = user_filename
	print "opening " + desktoppath + default_filename + "..."
	openfile = open(desktoppath + default_filename)
	stringified = mmap.mmap(openfile.fileno(), 0, access=mmap.ACCESS_READ)
	return stringified


# get_item_list attempts to generically return list of items from the xml
#
# the item_string is the file snippet
# the item_xml_name marks the start of the "Collection" in the xml
# the xml_before is any tag that can be used to find the item start
# the pad is the character distance from the xml_before tag to the text you want
# same for the xml_end

def get_item_list(item_string,item_xml_name,item_xml_elem,xml_before,pad_before,xml_after,pad_after):
	item_startpos = item_string.find('<' + item_xml_name + 'Collection>')
	item_endpos = item_string.find('</' + item_xml_name + 'Collection>')
	item_string = item_string[item_startpos:item_endpos]
	listindex = 0
	item_list = []
	while item_string.find(item_xml_elem) != -1:
		thisitem_start = item_string.find(item_xml_elem) + len(item_xml_elem)
		item_string = item_string[thisitem_start:]
		thisitem_start = item_string.find(xml_before) + pad_before
		thisitem_end = item_string.find(xml_after) - pad_after
		item_list.append(listindex)
		item_list[listindex] = item_string[thisitem_start:thisitem_end]
		print item_list[listindex]
		item_string = item_string[thisitem_end + len(item_xml_name):]
		listindex = listindex + 1

# takes file string as input and returns a list with themes as output
# assumes each theme is theme id = index of returned list

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




filestring = getthefile('export.xml')
theme_list = get_item_list(filestring,'theme','<theme ','<title>',16,'</title>',3)
stream_list = get_item_list(filestring,'stream','<stream ','<title>',16,'</title>',3)
team_list =  get_item_list(filestring,'team','<team ','<title>',16,'</title>',3)
initiatives_list = get_item_list(filestring,'workItem','plan-initiatives-1','<title>',16,'</title>',3)




