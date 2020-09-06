def getPrefix(word):
    if len(word) >= 4:
        return word[:4]
    elif len(word) >= 3:
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


