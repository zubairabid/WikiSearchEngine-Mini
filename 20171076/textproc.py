from stopwords import notstopword
from stemmer import CStemmer

stemmer = CStemmer()

def nlppipe(listofwords):
    listofwords = list(filter(lambda x: x != '', listofwords)) 
    #listofwords = list(filter(lambda x: len(x) != 2, listofwords)) 
    lowercased = list(map(lambda x: x.lower(), listofwords))
    nonstop = list(filter(notstopword, lowercased))
    stemmed = stemmer.stemWords(nonstop)
    processedwords = stemmed
    return processedwords
