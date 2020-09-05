import re
import sys
import time
import pickle
from bisect import bisect_left

import xml.sax

from stopwords import st, notstopword
from tokenizer import custometoke
from wikitextparser import getCategory, getCitations, getInfobox, getLinks, \
        getPlaintext, isComment
from textproc import nlppipe
from textproc import anglicise

class WikiHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

        # Tracks which element is currently being parsed
        self.currElem = '' 

        # We also track if we're inside a <revision> context which contains all
        # the text of the article
        self.resetState()

        self.articlecount = 0
        self.time = time.time()

    def resetState(self):
        self.inText = False
        self.rawtxt = ''

        self.inInfobox = False
        self.inLink = False
        self.inCategory = False
        self.count = 0

        self.title = ''
        self.body = ''
        self.categories = ''
        self.infobox = ''
        self.references = ''
        self.links = ''

    def createIndex(self):
        global index
        words = {}
        for word in self.title:
            if word in words:
                if 'title' in words[word]:
                    words[word]['title'] += 1
                else:
                    words[word]['title'] = 1
            else:
                words[word] = {'title': 1}

        for word in self.body:
            if word in words:
                if 'body' in words[word]:
                    words[word]['body'] += 1
                else:
                    words[word]['body'] = 1
            else:
                words[word] = {'body': 1}

        for word in self.categories:
            if word in words:
                if 'cat' in words[word]:
                    words[word]['cat'] += 1
                else:
                    words[word]['cat'] = 1
            else:
                words[word] = {'cat': 1}

        for word in self.infobox:
            if word in words:
                if 'info' in words[word]:
                    words[word]['info'] += 1
                else:
                    words[word]['info'] = 1
            else:
                words[word] = {'info': 1}

        for word in self.references:
            if word in words:
                if 'ref' in words[word]:
                    words[word]['ref'] += 1
                else:
                    words[word]['ref'] = 1
            else:
                words[word] = {'ref': 1}

        for word in self.links:
            if word in words:
                if 'link' in words[word]:
                    words[word]['link'] += 1
                else:
                    words[word]['link'] = 1
            else:
                words[word] = {'link': 1}

        for word in words:
            counts = words[word]
            addon = ''
            for area in counts:
                addon += area[:1] + str(counts[area])
            if word in index:
                index[word].append(str(self.articlecount)+addon)
            else:
                index[word] = [str(self.articlecount)+addon, ]

    def startElement(self, name, attrs):
        '''
        We use this to start tracking any variables we want to, like setting the
        current element, and enabling aggregation of text
        '''
        self.currElem = name

        if name == 'revision':
            self.inText = True

    def endElement(self, name):
        '''
        We use this function to reset all trackers, like the current element and
        text aggregation vars.
        '''
        if name == 'revision':
            self.mapIdToArticle()
            self.process()
            self.preprocess()
            self.createIndex()
            self.resetState()

        self.currElem = ''

    def characters(self, data):
        '''
        Data inside <tags> are collected in this function
        '''
        if self.currElem == 'title':
            self.title = data
            self.articlecount += 1
            if self.articlecount % 100 == 0:
                print(self.articlecount)
                print(time.time() - self.time)
                self.time = time.time()

        if self.inText and self.currElem == 'text':
            self.rawtxt += data

    def mapIdToArticle(self):
        global idArt
        idArt[self.articlecount] = self.title

    def setContexts(self, line):
        self.inCategory = False

        # Set contexts based on what's active
        if line.startswith('[[Category:'):
            self.inCategory = True
            self.inLink = False
        elif 'External links' in line:
            self.inLink = True
        elif line.startswith('{{Infobox') or line.startswith('{{infobox'):
            self.inLink = False
            if self.count == 0:
                self.count = 0
            self.inInfobox = True
        elif line.startswith('=='):
            self.inLink = False

    def getValues(self, line):
        # If Category context, add the category.
        # If it's in the infobox context, add the Infobox content and keep
        # checking for citations. 
        # If it's in the Link context, add the links
        # Else, add the formatted plaintext

        if self.inCategory:
            self.categories += getCategory(line)
        elif self.inInfobox:
            self.count += (line.count('{') - line.count('}'))
            if self.count == 0:
                self.inInfobox = False
            values = getInfobox(line)
            re.sub(r"{{[Cc]ite(.+?)}}", "", values)
            self.references += getCitations(values)
            self.infobox += values
        elif self.inLink:
            values = getLinks(line)
            re.sub(r"{{[Cc]ite(.+?)}}", "", values)
            self.references += getCitations(values)
            self.links += getLinks(line)
        else:
            re.sub(r"{{[Cc]ite(.+?)}}", "", line)
            self.references += getCitations(line)
            self.body += getPlaintext(line)

    def process(self):
        # We will go through self.rawtxt line by line
        for line in self.rawtxt.split('\n'):
            line = line.strip()
            if isComment(line):
                continue
            self.setContexts(line)
            self.getValues(line)

    def preprocess(self):
        global totaltoken
        # Tokenise a text
        # Stopwordremoval, lowercasing, stemming
        self.title = custometoke(self.title)
        totaltoken += len(self.title)
        self.title = anglicise(self.title)
        self.title = nlppipe(self.title)
        
        self.body = custometoke(self.body)
        totaltoken += len(self.body)
        self.body = anglicise(self.body)
        self.body = nlppipe(self.body)

        self.infobox = custometoke(self.infobox)
        totaltoken += len(self.infobox)
        self.infobox = anglicise(self.infobox)
        self.infobox = nlppipe(self.infobox)

        self.categories = custometoke(self.categories)
        totaltoken += len(self.categories)
        self.categories = anglicise(self.categories)
        self.categories = nlppipe(self.categories)

        self.links = custometoke(self.links)
        totaltoken += len(self.links)
        self.links = anglicise(self.links)
        self.links = nlppipe(self.links)

        self.references = custometoke(self.references)
        totaltoken += len(self.references)
        self.references = anglicise(self.references)
        self.references = nlppipe(self.references)


index = {}
idArt = {}
totaltoken = 0

if __name__ == "__main__":
    
    # Recording the start time to report on time taken
    time_init = time.time()

    # The path of dataset and outputs are taken from user input
    path_to_wiki_dump = sys.argv[1]
    path_to_inverted_index_out = sys.argv[2]
    path_to_inv_statfile_out = sys.argv[3]

    print(
            path_to_wiki_dump,
            path_to_inverted_index_out,
            path_to_inv_statfile_out
    )

    handler = WikiHandler()
    xml.sax.parse(path_to_wiki_dump, handler)

    print(totaltoken)
    print(len(index))
    with open(path_to_inv_statfile_out, 'w') as f:
        f.write(str(totaltoken) + '\n')
        f.write(str(len(index)) + '\n')

    #with open(path_to_inverted_index_out, 'wb') as f:
    #    pickle.dump(index, f)
    with open(path_to_inverted_index_out, 'w') as f:
        for key in sorted(index.keys()):
            wrt = key
            for val in index[key]:
                wrt += ';' + val
            wrt += '\n'
            f.write(wrt)


    # Recording the end time to report on the time taken
    time_end = time.time()

    print(time_end - time_init)
        
