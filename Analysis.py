import re

## Read a TSV file (same as they use for the SPSs) into a dictionary of sensor readings.
# @param filename The path to the TSV (or XLS) file to parse
# @return A dictionary indexed by sensor name with arrays of sensor data
def read_tsv(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    title_line_number = find_first_non_empy_line(lines)
    titles = parse_line(lines[title_line_number].replace('\n', ''))

    dictionary = dict()

    for title in titles:
        dictionary[title] = []

    for index in range(title_line_number+1, len(lines)):
        data = parse_line(lines[index].replace('\n', ''))
        for d_index in range(0,len(data)):
            dictionary[titles[d_index]].append(data[d_index])
    
    return dictionary
    
## Parse a single line of tsv, allowing columns to be empty to comply with the formatting of the SPS's fields
# @param line The line in a string
# @return An array of data representing data from each column of the spreadsheet
def parse_line(line):
    prev_i = 0
    i = 0
    entries = []
    while i <= len(line):
        if i >= len(line) or line[i] in "\t\n":
            entries.append(line[prev_i:i])
            prev_i = i + 1
        i += 1
    return entries

## Find the first non empty line in a list of lines (useful for finding the title line in the SPS's files)
# @param lines The array of lines to find the first used line in
# @return The line number of the first used line
def find_first_non_empy_line(lines):
    ret = 0
    while lines[ret].replace('\n','') is "":
        ret += 1
    return ret

# Example Usage
# print(read_tsv('C:\\Users\\c-duffy\\Documents\\F016_20171203_000002.xls')['01_Saus1'][3])