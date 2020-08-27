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
        self.inText = False 
        self.article = ''

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
            self.inText = False
            print("Article text: ", self.article)
            self.article = ''

        self.currElem = ''

    def characters(self, data):
        '''
        Data inside <tags? are collected in this function
        '''
        if self.currElem == 'title':
            print('\n'*10,'#'*100)
            print("Title: ", data)

        if self.inText and self.currElem == 'text':
            self.article += data

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
        
