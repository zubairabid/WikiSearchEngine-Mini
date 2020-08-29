import re
citematch = re.compile(r'{{[Cc]ite(.+?)}}')

def isComment(line):
    return line.startswith('<!--')

def getCategory(line):
    PREFIX_LENGTH = 11 # length of [[Category:
    return line[PREFIX_LENGTH:-2] + ' '

def getCitations(line):
    # if any <ref> in line, extract
    # if any <cite> in line, extract
    # for each reference:
        # 
    allrefs = citematch.findall(line)
    cites = ''
    for ref in allrefs:
        citesent = ''
        splits = ref.split('|')
        for split in splits:
            word = split
            if '=' in split:
                word = split[split.find('=')+1:]
            word = word.strip()
            citesent += word + ' '
        cites += citesent + ' '

    return cites

def getInfobox(line):
    # Trim the line first.
    # Each infobox either starts with a |, }, or {. All else can be ignored.
    # If |, the line after '=' should be taken
    # If {, the line after box should be taken
    # If }, ignore
    returnval = ''
    if line.startswith('|'):
        returnval = line[line.find('=')+1:].strip() + ' '
    elif line.startswith('{'):
        returnval = line[line.find(' '):].strip() + ' '
    else:
        pass
    return returnval

def getLinks(line):
    if not line.startswith('=='):
        return line + ' '
    else:
        return ''

def getPlaintext(line):
    return line

