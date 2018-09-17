import re

def read_tsv(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    title_line_number = find_first_non_empy_line(lines)
    # titles = lines[title_line_number].replace('\n','').split()
    titles = parse_line(lines[title_line_number].replace('\n', ''))

    dictionary = dict()

    for title in titles:
        dictionary[title] = []

    for index in range(title_line_number+1, len(lines)):
        data = parse_line(lines[index].replace('\n', ''))
        for d_index in range(0,len(data)):
            dictionary[titles[d_index]].append(data[d_index])
    
    return dictionary
    
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

def find_first_non_empy_line(lines):
    ret = 0
    while lines[ret].replace('\n','') is "":
        ret += 1
    return ret

# print(read_tsv('C:\\Users\\c-duffy\\Documents\\F016_20171203_000002.xls')['01_Saus1'][3])