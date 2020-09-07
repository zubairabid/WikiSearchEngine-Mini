from otherproc import getPrefix, parseLine
from textproc import nlppipe
import pickle
import time
import math
import sys
import re

def get_id(res):
    return re.findall(r'[0-9]+|[a-z]', res)[0]

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

print("loading mapping")
t = time.time()
path_to_mapping = '../Out/Index/mapping.pkl'
with open(path_to_mapping, 'rb') as f:
    mapping = pickle.load(f)
print("mapping loaded", time.time()-t)

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
    search = search[:-1]
    search = search.split(', ')
    k = int(search[0])
    terms = search[1].split(' ')

    all_results = []
    all_results_tf = []
    field = False
    fd = ''
    
    print('\nSearching: ', search)
    searchtime = time.time()
    finterms = [] # Keeps track of all the final terms used for search
    tfmap = {} # Keeps track of all tf-idf scores for word-doc pairs

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
            t = time.time()
            searchterm = searchterm[0]
            finterms.append(searchterm)
            prefix = getPrefix(searchterm)

            print("Searching for ", searchterm)
            # load the file,
            #   read it line by line until you meet the answer,
            #       for each posting check if field is satisfied, and add
            #       get tf-idf for each and sort

            # Loading the index file
            with open('../Out/Index/'+prefix+'.txt', 'r') as f:

                # Reading it line by line 
                for line in f:
                    key, vals, dud = parseLine(line, 0)
                    if key != searchterm:
                        continue

                    # Once the answer is found, run the search for
                    # field/nonfield
                    if field:
                        for val in vals:
                            if fd in val:
                                term_results.append(val)
                        n_app = len(term_results)
                        # n_app = len(vals)

                        for res in term_results:
                            tfidf = tf_idf(res, n_app, True, fd)
                            term_results_tf.append((tfidf, get_id(res)))
                            tfmap[(get_id(res), searchterm)] = tfidf
                    else:
                        term_results = vals
                        n_app = len(term_results)

                        for res in term_results:
                            tfidf = tf_idf(res, n_app)
                            term_results_tf.append((tfidf, get_id(res)))
                            tfmap[(get_id(res), searchterm)] = tfidf
                    break
                
            term_results_tf.sort(reverse=True)
            all_results.append(set([res[1] for res in term_results_tf]))
            all_results_tf += term_results_tf
            #print(term_results_tf[:k])
            for i in range(k):
                if i < len(term_results_tf):
                    print(term_results_tf[i][0], end=' ')
                    articleid = term_results_tf[i][1]
                    print(mapping[articleid])
            print(time.time() - t)
    
    if len(all_results) > 0:
        print("TOTAL")
        res = set(all_results[0])
        for termres in all_results:
            res = res & termres
        print(len(res))
        tmpresults = []
        for t in res:
            score = 0
            for word in finterms:
                score += tfmap[(t, word)]
            tmpresults.append((score, t))
        tmpresults.sort(reverse=True)
        if len(tmpresults) >= k:
            for i in range(k):
                print(tmpresults[i][1], mapping[tmpresults[i][1]])
        else: # drought
            all_results_tf.sort(reverse=True)
            kleft = k - len(tmpresults)
            alli = 0
            while kleft > 0 and alli < len(all_results_tf):
                if all_results_tf[alli][1] not in res:
                    kleft -= 1
                    print(all_results_tf[alli][1], mapping[all_results_tf[alli][1]])
                alli += 1
    else:
        print("No results")
    print("Total time: ", time.time() - searchtime)

