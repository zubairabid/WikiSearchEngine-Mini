def isSpecial(prefix):
    return prefix == '201' or \
            prefix == '200' or \
            prefix == 'con' or \
            prefix == 'com' or \
            prefix == 'pro' or \
            prefix == 'sta' or \
            prefix == 'ref' or \
            prefix == 'dis' or \
            prefix == 'red' or \
            prefix == 'mar' or \
            prefix == 'htt' or \
            prefix == 'cha' or \
            prefix == 'pre'

def getPrefix(word):
    if len(word) >= 4:
        if isSpecial(word[:3]):
            return word[:4]
        return word[:3]
    elif len(word) >= 3:
    #if len(word) >= 3:
        return word[:3]
    elif len(word) >= 2:
        return word[:2]
    else:
        return word[:1]

def parseLine(line, fileno):
    split = line.split(';')
    key = split[0]
    vals = split[1:]
    vals[-1] = vals[-1][:-1]
    return (key, vals, fileno)


