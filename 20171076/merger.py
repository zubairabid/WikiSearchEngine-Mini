import pickle

z = ord('0')
def replacenum(value, offset):
    ret = ''
    for i in value:
        x = ord(i) - z
        if x < 0 or x > 9:
            ret = str(int(ret)+offset) + value
            break
        else:
            ret += i
            value = value[1:]
    return ret

def parseLine(line, offset):
    split = line.split(';')
    key = split[0]
    vals = split[1:]
    for i in range(len(vals)):
        val = vals[i]
        vals[i] = replacenum(val, offset)
    return key, vals

F_COUNT = 34
DATA_ROOT = '../Out/'

INDEX_PREFIX = 'ind'

init_ind_names = [INDEX_PREFIX+str(i)+'.txt' for i in range(1,F_COUNT+1)]

# Paths to indexes and dictionaries
init_ind_paths = [DATA_ROOT+indexname for indexname in init_ind_names]
docid_art_paths = [indexpath+'dict.pkl' for indexpath in init_ind_paths]

# fetch docArt matches, and offsets
docid_art_all = []
docid_offset = []
cumulative_offset = 0
for docid_art_path in docid_art_paths:
    with open(docid_art_path, 'rb') as f:
        tmpdict = pickle.load(f)
        cumulative_offset += list(tmpdict.keys())[-1]
    
        docid_art_all.append(tmpdict)
        docid_offset.append(cumulative_offset)

# Update docid-article matches
for i in range(1, F_COUNT):
    offset = docid_offset[i-1]
    for old_key in docid_art_all[i].keys():
        docid_art_all[i][old_key+offset] = docid_art_all[i].pop(old_key)

# Make a list of all filepointers
init_ind_fps = []
for init_ind_path in init_ind_paths:
    init_ind_fps.append(open(init_ind_path, 'r'))
