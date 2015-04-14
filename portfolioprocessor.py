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

# get_item_list returns list of items from the xml
# by "items" I mean initiatives, releases, teams, etc
#
# the item_string is the relevant file snippet with the item list
# the item_xml_name marks the start of the item "Collection" in the xml
# the xml_before is any tag that can be used to find each specific item start
# the pad is the character distance from the xml_before tag to the text you want
# same for the xml_end

def get_item_list(
	item_string,
	item_xml_name,
	item_xml_elem,
	xml_before,
	pad_before,
	xml_after,
	pad_after):
	item_startpos = item_string.find('<' + item_xml_name + 'Collection>')
	item_endpos = item_string.find('</' + item_xml_name + 'Collection>')
	item_string = item_string[item_startpos:item_endpos]
	item_list = []
	i = 0
	while item_string.find(item_xml_elem) != -1:
		item_start = item_string.find(item_xml_elem) + len(item_xml_elem)
		item_string = item_string[item_start:]
		item_start = item_string.find(xml_before) + pad_before
		item_end = item_string.find(xml_after) - pad_after
		item_list.append(i)
		item_list[i] = item_string[item_start:item_end]
		print item_list[i]
		item_string = item_string[item_end + len(item_xml_name):]
		i = i + 1

def get_item_list_2D(
	item_string,
	item_xml_name,
	item_xml_elem,
	xml_before,
	pad_before,
	xml_after,
	pad_after,
	xml_2D_elem):
	list_startpos = item_string.find('<' + item_xml_name + 'Collection>')
	list_endpos = item_string.find('</' + item_xml_name + 'Collection>')
	item_string = item_string[list_startpos:list_endpos]
	item_list = []
	item_list.append([])
	item_list.append([])
	i = 0
	j = 0
	while item_string.find(item_xml_elem) != -1:
		item_start = item_string.find(item_xml_elem) + len(item_xml_elem)
		item_string = item_string[item_start:]
		firstindex_loc = item_string.find(xml_2D_elem) + len(xml_2D_elem) + 2
		last_i = i
		i = int(item_string[firstindex_loc:firstindex_loc+1]) - 1
		if last_i != i: j = 0
		item_start = item_string.find(xml_before) + pad_before
		item_end = item_string.find(xml_after) - pad_after
		print i
		print j
		item_list[i].append(j)
		item_list[i][j] = item_string[item_start:item_end]
		print item_list[i][j]
		item_string = item_string[item_end + len(item_xml_name):]
		j = j + 1


# Get all our lists

filestring = getthefile('export.xml')
theme_list = get_item_list(filestring,'theme','<theme ','<title>',16,'</title>',3)
stream_list = get_item_list(filestring,'stream','<stream ','<title>',16,'</title>',3)
team_list =  get_item_list(filestring,'team','<team ','<title>',16,'</title>',3)
initiatives_list = get_item_list(filestring,'workItem','plan-initiatives-1','<title>',16,'</title>',3)
releases_list = get_item_list_2D(filestring,'release','<release ','<title>',16,'</title>',3,'aostream')




