import sys
import time

import xml.sax


class WikiHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

        # Tracks which element is currently being parsed
        self.currElem = '' 

        # We also track if we're inside a <revision> context which contains all
        # the text of the article
        self.resetState()

        self.articlecount = 0

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
            self.process()
            self.preprocess()
            #print("Title: ", self.title)
            #print("Article text: \n", "-"*100, "\n", self.rawtxt)
            #print("Infobox:\n", "-"*100, "\n", self.infobox)
            #print("Categories:\n", "-"*100, "\n", self.categories)
            #print("Links:\n", "-"*100, "\n", self.links)
            #print("Refs:\n", "-"*100, "\n", self.references)
            self.resetState()

        self.currElem = ''

    def characters(self, data):
        '''
        Data inside <tags> are collected in this function
        '''
        if self.currElem == 'title':
            self.title = data
            self.articlecount += 1
            if self.articlecount % 1000 == 0:
                print(self.articlecount)

        if self.inText and self.currElem == 'text':
            self.rawtxt += data

    def process(self):
        # We will go through self.rawtxt line by line
        for line in self.rawtxt.split('\n'):
            line = line.strip()
            if isComment(line):
                continue
            self.setContexts(line)
            self.getValues(line)
            # append preprocess(categories)
            # append preprocess(citations)
            # append preprocess(links)
            # append preprocess(plaintext)

    def preprocess(self):
        # print(word_tokenize(self.references))
        # print('\n')
        # print(custometoke(self.references))

        # Tokenise a text
        # Stopwordremoval, lowercasing, stemming
        nlpwork(custometoke(self.body))
        nlpwork(custometoke(self.infobox))
        nlpwork(custometoke(self.categories))
        nlpwork(custometoke(self.links))
        nlpwork(custometoke(self.references))

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
            self.references += getCitations(values)
            self.infobox += values
        elif self.inLink:
            values = getLinks(line)
            self.references += getCitations(values)
            self.links += getLinks(line)
        else:
            self.references += getCitations(line)
            self.body += getPlaintext(line)

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

def isComment(line):
    return line.startswith('<!--')

from nltk.corpus import stopwords
def notstopwords(word):
    return not word in stopwords

#import Stemmer
#stemmer = Stemmer.Stemmer('english')

def nlpwork(listofwords):
    nonstop = list(filter(notstopwords, listofwords))
    lowercased = list(map(lambda x: x.lower(), nonstop))
    # stemmed = list(map(stemmer.stemWords, lowercased))

def getCategory(line):
    PREFIX_LENGTH = 11 # length of [[Category:
    return line[PREFIX_LENGTH:-2] + ' '

from nltk.tokenize import word_tokenize

def custometoke(line):
    return re.findall(r'[\U00010000-\U0010ffff]'\
            r'|[A-Z0-9a-z]+[A-Z0-9a-z._%+-]*@[A-Z0-9a-z]+(?:\.[A-Z0-9a-z]+)+'\
            r'|(?<= )[$€£¥₹]?[0-9]+(?:[,.][0-9]+)*[$€£¥₹]?'\
            r'|(?:(?:https?:\/\/(?:www.)?)|www.)[A-Z0-9a-z_-]+(?:\.[A-Z0-9a-z_\/-]+)+'\
            #r'|(?:(?<=[^A-Za-z0-9])|^)@[A-Z0-9a-z._+]+[A-Za-z0-9_]'\
            #r'|#[A-Za-z0-9]+(?:[\._-][A-Za-z0-9]+)*'\
            #r'|\.{3,}'\
            #r'|[!"#$%\&\'()*+,\-.:;<=>?@\[\\\/\]\^_`{\|}~]'\
            r'|[A-Z]\.'\
            r'|\w+', line)

import re
citematch = re.compile(r'{{[Cc]ite(.+?)}}')

def getCitations(line):
    # if any <ref> in line, extract
    # if any <cite> in line, extract
    # for each reference:
        # 
    allrefs = citematch.findall(line)
    cites = ''
    for ref in allrefs:
        citesent = ''
        splits = ref.split('|')
        for split in splits:
            word = split
            if '=' in split:
                word = split[split.find('=')+1:]
            word = word.strip()
            citesent += word + ' '
        cites += citesent + ' '

    return cites

def getInfobox(line):
    # Trim the line first.
    # Each infobox either starts with a |, }, or {. All else can be ignored.
    # If |, the line after '=' should be taken
    # If {, the line after box should be taken
    # If }, ignore
    returnval = ''
    if line.startswith('|'):
        returnval = line[line.find('=')+1:].strip() + ' '
    elif line.startswith('{'):
        returnval = line[line.find(' '):].strip() + ' '
    else:
        pass
    return returnval

def getLinks(line):
    if not line.startswith('=='):
        return line + ' '
    else:
        return ''

def getPlaintext(line):
    return line

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

    # Recording the end time to report on the time taken
    time_end = time.time()

    print(time_end - time_init)
        
