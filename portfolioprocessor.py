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

def getthefile(default_filename):
    print 'Inside user home folder ~'
    homepath = os.path.expanduser('~')
    user_filename = raw_input(
        "Enter name of file or path (hit enter for Desktop/" +
            default_filename + "): ")
    if user_filename != '':
        file_to_load = homepath + user_filename
    else:
        file_to_load = homepath + "/Desktop/" + default_filename
    print ''
    print "opening " + file_to_load + "..."
    openfile = open(file_to_load)
    return openfile


# returnfileasstring() returns an mmap string of the file for parsing

def returnfileasstring(openfile):
    stringified = mmap.mmap(openfile.fileno(), 0, access=mmap.ACCESS_READ)
    return stringified


# trim_to_section()
# Pick out the section of the file to work on during each processing chunk
# this prevents any term collisions during processing

def trim_to_section(item_string, item_xml_name):
    item_startpos = item_string.find('<' + item_xml_name + 'Collection>')
    item_endpos = item_string.find('</' + item_xml_name + 'Collection>')
    return item_string[item_startpos:item_endpos]


# get_item_list() returns list of items from the xml
# by "items" I mean initiatives, releases, teams, etc
#
# the item_string is the relevant file snippet with the item list
# the item_xml_name marks the start of the item "Collection" in the xml
# the xml_before is any tag that can be used to find each specific item start
# the pad is the character distance from the xml_before tag to the text you want
# same for the xml_end
#
# you could probably re-write these to use parser but it works and is flexible

def get_item_list(
        item_string,
        item_xml_name,
        item_xml_elem,
        xml_before,
        pad_before,
        xml_after,
        pad_after):
    item_string = trim_to_section(item_string, item_xml_name)
    item_list = []
    i = 0
    while item_string.find(item_xml_elem) != -1:
        item_start = item_string.find(item_xml_elem) + len(item_xml_elem)
        item_string = item_string[item_start:]
        item_start = item_string.find(xml_before) + pad_before
        item_end = item_string.find(xml_after) - pad_after
        item_list.append(i)
        item_list[i] = item_string[item_start:item_end]
#debug      print item_list[i]
        item_string = item_string[item_end + len(item_xml_name):]
        i = i + 1
    print "Found", len(item_list), item_xml_name + "s..."
    return item_list


# parsefileasxml() uses parser to pull out the epics and associated
# characteristic ids then uses the lists we pulled earlier to turn the ids into
# words (release names etc).
# Note: type = 0 means portfolio epic, type=1 means portfolio story,
# type = 2 means initiative
# The loop first uses the entry ids then replaces them with the real priority
# So, final state for toplevellist structure: 
# [priority, portfolio epic subj, [team epic subj, stream, release, theme]]

def parsefileasxml(openfile, theme_list, stream_list,
                   team_list, initiative_list, release_list):
  #  xml_file = ET.parse(openfile)
    parsed_xml_file = ET.parse(openfile).getroot()
    top_level_list = []
    top_level_list.append([])
    priorityref = []
    i = 0
    for work_item in parsed_xml_file.iter('workItem'):
        entry_type = work_item.attrib.get('type')
        entry_id = work_item.attrib.get('id')
        entry_parent = work_item.attrib.get('aoparent')
        entry_subj = work_item.find('title').text
        entry_stream = ''
        entry_release = ''
        entry_theme = ''
        if entry_type and entry_id and entry_subj:
            if entry_type == "0":
                top_level_list[i] = [entry_id, entry_subj, [[]]]
                top_level_list.append([[]])
                priorityref.append(entry_id)
                i = i + 1
            elif entry_type == "1":
                entry_stream = work_item.attrib.get('aostream')
                if entry_stream:
                    entry_stream = stream_list[int(entry_stream) - 1]
                entry_release = work_item.attrib.get('aorelease')
                if entry_release:
                    entry_release = release_list[int(entry_release) - 1]
                entry_theme = work_item.attrib.get('aotheme')
                if entry_theme:
                    entry_theme = theme_list[int(entry_theme) - 1]
                top_level_list[priorityref.index(entry_parent)][2].append(
                    [entry_subj, entry_stream, entry_release, entry_theme])
                i = i + 1
#            print entry_type, entry_id, entry_parent, entry_stream, entry_release, entry_subj
    print "Found", len(top_level_list), "epics..."
    return top_level_list


# generate_csv() writes out all of our parsing to CSV file in the output folder on desktop

def generate_csv(complete_data_list):
    file_name = 'portfolio-' + str(
        datetime.datetime.now().strftime("%Y%m%d%H%M")) + '.csv'
    path_name = os.path.expanduser('~/Desktop/') + 'output/'
    print ''
    print 'Output to ' + path_name + file_name
    print ''
    csvfile = open(os.path.join(path_name, file_name), 'a+')
    output_file = csv.writer(csvfile)
    output_file.writerow(['Priority', 'Portfolio Epic', 'Team Epic', 
                          'Stream', 'Release', 'Theme', 'Initiative'])
    i = 0
    lineswritten = 0
    for lineitem in complete_data_list:
        i = i + 1
#debug      print i, lineitem
        try:
            for subline in lineitem[2]:
                try:
                    output_file.writerow([i, lineitem[1], subline[0],
                                         subline[1], subline[2], subline[3]])
                    lineswritten = lineswritten + 1
                except IndexError:
                    output_file.writerow([i, lineitem[1]])
                    lineswritten = lineswritten + 1
        except IndexError:
            output_file.writerow([i])
            lineswritten = lineswritten + 1
    print "Wrote", i, "portfolio epics", "and", lineswritten, "lines to your output file"


# main() methodically gets all our lists, consolidates them, and then output them to the csv file

def main():
    openfile = getthefile('export.xml')
    print ''
    print "Don't forget your output folder with proper permissions per readme.txt"
    print ''
    filestring = returnfileasstring(openfile)
    theme_list = get_item_list(filestring, 'theme', '<theme ', '<title>', 16,
                               '</title>', 3)
    stream_list = get_item_list(filestring, 'stream', '<stream ', '<title>', 16,
                                '</title>', 3)
    print "streams:", stream_list
    team_list = get_item_list(filestring, 'team', '<team ', '<title>', 16,
                              '</title>', 3)
    initiative_list = get_item_list(filestring, 'workItem',
                                    'plan-initiatives-1', '<title>', 16, '</title>', 3)
    release_list = get_item_list(filestring, 'release', '<release ', '<title>',
                                 16, '</title>', 3)
    print "releases:", release_list
    complete_data_list = parsefileasxml(openfile, theme_list, stream_list,
        team_list, initiative_list, release_list)
    generate_csv(complete_data_list)

if __name__ == "__main__": 
    main()



# Note if you want to make this executable with just the file name:
# make the file executable:
# chmod +x portfolioprocessor.py
# and put it in a directory on your PATH (can be a symlink):
# export PATH=/my/directory/with/pythonscript:$PATH
# For permanence add that at the bottom of your .bashrc or .bash_profile
