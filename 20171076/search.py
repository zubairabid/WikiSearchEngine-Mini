from textproc import nlppipe
import sys

#with open('./ind.pkl', 'rb') as f:
#    table = pickle.load(f)

print("Loading the index. This will take a while...")
path_to_inverted_index_out = sys.argv[1]
index = {}
with open(path_to_inverted_index_out, 'r') as f:
    for line in f:
        split = line.split(';')
        index[split[0]] = split[1:]
        index[split[0]][-1] = index[split[0]][-1][:-1] 

field = False
fd = ''
terms = sys.argv[2:]

for term in terms:
    if term.startswith('t:') or term.startswith('i:') or term.startswith('r:')\
            or term.startswith('l:') or term.startswith('c:') \
            or term.startswith('b:'):
        field = True
        fd = term[0]
        term = term[2:]
    searchterm = nlppipe([term,])
    if searchterm != []:
        searchterm = searchterm[0]
        print("Searching for ", searchterm, " after preprocessing")
        processedterm = searchterm
        if processedterm in index:
            results = index[processedterm]
            if field:
                print("Searching within field: ", fd)
                found = False
                for val in results:
                    if fd in val:
                        found = True
                        break
                if found:
                    print(results)
                else:
                    print([])
            else:
                print(results)
        else:
            print([])
    else:
        print([])
