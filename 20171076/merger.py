import pickle
import heapq

from otherproc import getPrefix, parseLine

F_COUNT = 34
DATA_ROOT = '../Out/'
OUT_DATA_ROOT = '../Out/Index/'
INDEX_PREFIX = 'ind'

init_ind_names = [INDEX_PREFIX+str(i)+'.txt' for i in range(1,F_COUNT+1)]

# Paths to indexes and dictionaries
init_ind_paths = [DATA_ROOT+indexname for indexname in init_ind_names]
docid_paths = [indexpath+'dict.pkl' for indexpath in init_ind_paths]

# fetch docArt matches
docids = {}
print("creating mappings")
for docid_path in docid_paths:
    with open(docid_path, 'rb') as f:
        tmpdict = pickle.load(f)
        docids = {**docids, **tmpdict}

with open(OUT_DATA_ROOT+'mapping.pkl', 'wb') as f:
    pickle.dump(docids, f)
print("mappings created")

# Make a list of all filepointers
init_ind_fps = []
for init_ind_path in init_ind_paths:
    init_ind_fps.append(open(init_ind_path, 'r'))

# Load all FPs in heap once
min_heap = []
for fno, fp in enumerate(init_ind_fps):
    line = fp.readline()
    if not line:
        continue
    heapq.heappush(min_heap, parseLine(line, fno))

# M E R G E
activeindex = {}
activeprefix = ''
tmp = 0
while len(min_heap) > 0:
    word = heapq.heappop(min_heap)

    # Add next line to the heap
    line = init_ind_fps[word[2]].readline()
    if line:
        heapq.heappush(min_heap, parseLine(line, word[2]))

    prefix = getPrefix(word[0])
    if prefix != activeprefix:
        if activeprefix != '':
            with open(OUT_DATA_ROOT+activeprefix+'.txt', 'w') as f:
                for key in activeindex:
                    wrt = key
                    for val in activeindex[key]:
                        wrt += ';' + val
                    wrt += '\n'
                    f.write(wrt)
            tmp += 1
            if tmp % 1000 == 0:
                print(activeprefix, ' indexed')
        activeprefix = prefix
        activeindex = {}

    if word[0] in activeindex.keys():
        activeindex[word[0]] += word[1]
    else:
        activeindex[word[0]] = word[1]
