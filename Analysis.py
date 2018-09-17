import re

def read_tsv(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    title_line_number = find_first_non_empy_line(lines)
    titles = lines[title_line_number].replace('\n','').split()

    dictionary = dict()

    for title in titles:
        dictionary[title] = []

    for index in range(title_line_number+1, len(lines)):
        # data = lines[index].replace('\n','').split()
        data = re.compile("\t").split(lines[index].replace('\n',''))
        for d_index in range(0,len(data)):
            dictionary[titles[d_index]].append(data[d_index])
    
    return dictionary
    
def find_first_non_empy_line(lines):
    ret = 0
    while lines[ret].replace('\n','') is "":
        ret += 1
    return ret

print(read_tsv("test.txt"))