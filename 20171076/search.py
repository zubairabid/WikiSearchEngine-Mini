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

print([term,])
print(nlppipe([term,]))
processedterm = nlppipe([term,])[0]
print(index[processedterm])
