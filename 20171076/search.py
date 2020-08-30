from textproc import nlppipe
import pickle
import sys

#with open('./ind.pkl', 'rb') as f:
#    table = pickle.load(f)

path_to_inverted_index_out = sys.argv[1]
index = {}
with open(path_to_inverted_index_out, 'r') as f:
    for line in f:
        split = line.split(';')
        index[split[0]] = split[1:]
        index[split[0]][-1] = index[split[0]][-1][:-1] 

term = input("Enter search term: ")
prefix = term[:2]

field = False
fd = ''
if prefix == 't:' or prefix == 'i:' or prefix == 'r:' or prefix == 'l:' or \
        prefix == 'c' or prefix == 'b':
    field = True
    fd = prefix[0]
    term = term[2:]

terms = term.split(' ')
searchterms = nlppipe(terms)
for searchterm in searchterms:
    if searchterm != []:
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
