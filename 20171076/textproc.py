import unicodedata
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

def anglicise(listofwords):
    newlist = ['']*len(listofwords)
    for i, word in enumerate(listofwords):
        nfkd_form = unicodedata.normalize('NFKD', word)
        nword = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
        newlist[i] = nword
    return newlist

