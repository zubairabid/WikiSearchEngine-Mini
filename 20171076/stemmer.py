#import Stemmer
from nltk.stem.snowball import SnowballStemmer
#from nltk.stem.porter import PorterStemmer

class CStemmer:
    def __init__(self):
        self.stems = {}
        #self.stemmer = Stemmer.Stemmer('english')
        self.stemmer = SnowballStemmer('english')
        #self.stemmer = PorterStemmer()

    def stemWords(self, words):
        retl = []
        for word in words:
            if not word in self.stems:
                #self.stems[word] = self.stemmer.stemWord(word)
                self.stems[word] = self.stemmer.stem(word)
            retl.append(self.stems[word])
        return retl
