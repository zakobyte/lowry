'''
Created on 30 Nov 2011

@author: Zak
'''

import os, os.path
import nltk

FILE_NAME = "../../repository/small_machines/Small_Machines.txt"

class ContentAnalyser():
    def __init__(self):
        pass
    
    def word_count(self):
        print self
    
    def frequency(self):
        pass
    
    def load_text(self, filename):
        nltk.text = open(FILE_NAME).read()
        print "Loaded the text file"
    
if __name__ == "__main__":
    ca = ContentAnalyser()
    ca.load_text(FILE_NAME)
    