from textproc import nlpwork
import pickle

with open('./ind.pkl', 'rb') as f:
    table = pickle.load(f)

term = input("Enter search term")

processedterm = nlpwork(list(term))[0]
print(table[processedterm])
