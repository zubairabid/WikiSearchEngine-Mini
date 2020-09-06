from merger import getPrefix, parseLine
from textproc import nlppipe
import pickle
import math
import sys
import re

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def tf(field_entry, field, fd):
    field_values = re.findall(r'[0-9]+|[a-z]', field_entry)
    term_freq = sum(map(int, filter(is_number, field_values)))
    return 1 + math.log(term_freq)

def idf(n_app):
    vanilla = N_doc/n_app
    return math.log(vanilla)

def tf_idf(field_entry, n_app, field=False, fd=''):
    return tf(field_entry, field, fd) * idf(n_app)

path_to_searchfile = sys.argv[1]
with open(path_to_searchfile, 'r') as f:
    searches = f.readlines()

path_to_mapping = '../Out/Index/mapping.pkl'
with open(path_to_mapping, 'rb') as f:
    mapping = pickle.load(f)

N_doc = len(mapping)

# print("Loading the index. This will take a while...")
# path_to_inverted_index_out = sys.argv[1]
# index = {}
# with open(path_to_inverted_index_out, 'r') as f:
    # for line in f:
        # split = line.split(';')
        # index[split[0]] = split[1:]
        # index[split[0]][-1] = index[split[0]][-1][:-1] 

for search in searches:
    search = search.split(' ')
    k = int(search[0])
    terms = search[1:]

    field = False
    fd = ''

    for term in terms:
        if term.startswith('t:') or term.startswith('i:') \
                or term.startswith('r:') or term.startswith('l:') \
                or term.startswith('c:') or term.startswith('b:'):
            field = True
            fd = term[0]
            term = term[2:]
        searchterm = nlppipe([term,])
        term_results = []
        term_results_tf = []
        if searchterm == []:
            pass # No result for this
        else:
            searchterm = searchterm[0]
            prefix = getPrefix(searchterm)

            print("Searching for ", searchterm)
            # load the file,
            #   read it line by line until you meet the answer,
            #       for each posting check if field is satisfied, and add
            #       get tf-idf for each and sort
            with open('../Out/Index/'+prefix+'.txt', 'r') as f:
                for line in f:
                    key, vals, dud = parseLine(line, 0)
                    if key != searchterm:
                        continue
                    if field:
                        for val in vals:
                            if fd in val:
                                term_results.append(val)
                        n_app = len(term_results)
                        # n_app = len(vals)
                        term_results_tf = [(tf_idf(res, n_app, True, fd), res) for res in term_results]
                    else:
                        term_results = vals
                        n_app = len(term_results)
                        term_results_tf = [(tf_idf(res, n_app), res) for res in term_results]
                    break
            term_results_tf.sort(reverse=True)
            print(term_results_tf)

