from stopwords import notstopword
from stemmer import CStemmer

stemmer = CStemmer()

def nlpwork(listofwords):
    listofwords = list(filter(lambda x: x != '', listofwords)) 
    nonstop = list(filter(notstopword, listofwords))
    lowercased = list(map(lambda x: x.lower(), nonstop))
    stemmed = stemmer.stemWords(lowercased)
    processedwords = stemmed
    return processedwords
