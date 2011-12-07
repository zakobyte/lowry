'''
Created on 7 Dec 2011

Example based on Python Text Processing with NLTK Cookbook 2.0

@author: Zak
'''
import pymongo
from nltk.data import LazyLoader
from nltk.tokenize import TreebankWordTokenizer
from nltk.util import AbstractLazySequence, LazyMap, LazyConcatenation

class MongoDBLazySequence(AbstractLazySequence):
    def __init__(self, host='localhost', port=27017, db='small_machines', collection='pages', field='content'):
        self.conn = pymongo.Connection(host, port)
        self.collection = self.conn[db][collection]
        self.field = field
    def __len__(self):
        return self.collection.count()
    
    def iterate_from(self, start):
        f = lambda d: d.get(self.field, '')
        return iter(LazyMap(f, self.collection.find(fields=[self.field], skip=start).sort("page_num", pymongo.ASCENDING)))
    
class MongoDBCorpusReader(object):
    def __init__(self, word_tokenizer=TreebankWordTokenizer(),
        sent_tokenizer=LazyLoader('tokenizers/punkt/english.pickle'), **kwargs):
        self._seq = MongoDBLazySequence(**kwargs)
        self._word_tokenize = word_tokenizer.tokenize
        self._sent_tokenize = sent_tokenizer.tokenize
    def text(self):
        return self._seq
    def words(self):
        return LazyConcatenation(LazyMap(self._word_tokenize, self.text()))
    def sents(self):
        return LazyConcatenation(LazyMap(self._sent_tokenize, self.text()))
    
if __name__ == "__main__":
    reader = MongoDBCorpusReader()
    

    for sent in reader.sents():
        print sent
        
    
    