#!/usr/bin/python
#
# portfolioprocessor.py 
#
# Goal of this is to process the XML output file exported from the
# Jira portfolio planner
# 

# Import necessary modules

import mmap
import os
import csv
import datetime
import xml.etree.ElementTree as ET

# getthefile()
# takes a default filename as the input and requests user input
# hardcoded to look on the mac desktop
# returns an mmap string of the file

def getthefile(default_filename):
	print 'Inside user ~/Desktop/'
	desktoppath = os.path.expanduser('~/Desktop/')
	user_filename = raw_input("Enter name of file (" + default_filename + "): ")
	if user_filename != '':
		default_filename = user_filename
	print "opening " + desktoppath + default_filename + "..."
	openfile = open(desktoppath + default_filename)
	stringified = mmap.mmap(openfile.fileno(), 0, access=mmap.ACCESS_READ)
	openfile.close()
	xml_file = ET.parse(desktoppath + default_filename)
	parsed_xml_file = xml_file.getroot()
#	for child in parsed_xml_file:
#		print child.tag, child.attrib
#	for work_item in parsed_xml_file.iter('workItem'):
#		print work_item.tag, work_item.attrib

# TODO: The below isn't working
	for work_item in parsed_xml_file.iter('workItem'):
		print "WHAT The fuCK"
		entry_num = work_item.attrib.get('type')
		entry_pri = work_item.attrib.get('aoparent')
		entry_subj = work_item.find('title').text
		print entry_num, entry_pri, entry_subj
		if entry_num and entry_pri and entry_subj:
			if entry_num == "0":
				print "Epic, pri " + entry_pri + ":" + entry_subj
			elif entry_num == "1":
				print "Story, pri " + entry_pri + ":" + entry_subj		
	return stringified
	print "TEAM LIST NEXT"
#TODO: Try to get item lists from parser instead:
	item_list = []
	i = 0
	for go_team in parsed_xml_file.iter('teamCollection'):
		print "go team"
		item_list.append(i)
		item_list[i] = go_team.find('title').text
		print item_list[i]
		i = i + 1

# Note: type = 0 means portfolio epic, type=1 means portfolio story, 
# type = 2 means initiative

# Pick out the section of the file to work on during each processing chunk
# this prevents any term collisions during processing

def trim_to_section(item_string,item_xml_name):
	item_startpos = item_string.find('<' + item_xml_name + 'Collection>')
	item_endpos = item_string.find('</' + item_xml_name + 'Collection>')
	return item_string[item_startpos:item_endpos]

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
	item_string = trim_to_section(item_string,item_xml_name)
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
	item_string = trim_to_section(item_string,item_xml_name)
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
		item_list[i].append(j)
		item_list[i][j] = item_string[item_start:item_end]
		print item_list[i][j]
		item_string = item_string[item_end + len(item_xml_name):]
		j = j + 1

# Process file

def generate_csv(
	item_string,
	theme_list,
	stream_list,
	team_list,
	initiatives_list,
	releases_list):
	item_string = trim_to_section(item_string,'workItem')
	file_name = 'portfolio-'+str(datetime.datetime.now().strftime("%Y%m%d%H%M"))+'.csv'
	path_name = os.path.expanduser('~/Desktop/') + 'output/'
	print 'Output to ' + path_name + file_name
	csvfile = open(os.path.join(path_name,file_name),'a+')
	output_file = csv.writer(csvfile)
	output_file.writerow(['Priority','Description','Theme','Initiative','Stream','Release'])
#	while item_string.find('</workItemCollection>') != -1:

# Get all our lists

def main():
	filestring = getthefile('export.xml')
	print 'You should create a folder on the desktop named "output"'
	print 'And give it permissions "chmod -R 755 output"'
	theme_list = get_item_list(filestring,'theme','<theme ','<title>',16,'</title>',3)
	stream_list = get_item_list(filestring,'stream','<stream ','<title>',16,'</title>',3)
	team_list =  get_item_list(filestring,'team','<team ','<title>',16,'</title>',3)
	initiatives_list = get_item_list(filestring,'workItem','plan-initiatives-1','<title>',16,'</title>',3)
	releases_list = get_item_list_2D(filestring,'release','<release ','<title>',16,'</title>',3,'aostream')
	generate_csv(filestring,theme_list,stream_list,team_list,initiatives_list,releases_list)

if __name__ == "__main__": main()

# Note if you want to make this executable with just the file name:
# make the file executable:
# chmod +x portfolioprocessor.py
# and put it in a directory on your PATH (can be a symlink):
# export PATH=/my/directory/with/pythonscript:$PATH
# For permanence add that at the bottom of your .bashrc or .bash_profile
