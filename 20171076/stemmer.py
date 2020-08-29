import Stemmer
class CStemmer:
    def __init__(self):
        self.stems = {}
        self.stemmer = Stemmer.Stemmer('english')

    def stemWords(self, words):
        retl = []
        for word in words:
            if not word in self.stems:
                self.stems[word] = self.stemmer.stemWord(word)
            retl.append(self.stems[word])
        return retl
