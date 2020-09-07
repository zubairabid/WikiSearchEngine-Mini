# Index creation:

- `wiki_indexer` creates the index for a single XML dump
- `par_indexer.sh` runs wiki_indexer for all files. Paths are taken as static
- `merger.py` takes the 34 created index files and merges them into the combined
  index splits.

# Search:

- `search.py` takes a file of search input and returns the output

# Helper code

- `stemmer.py`: Stemmer
- `tokenizer.py`: Tokenizer
- `stopwords.py`: Stopwords
- `textproc.py`: NLP pipeline Work
- `otherproc.py`: Helper code for IR
