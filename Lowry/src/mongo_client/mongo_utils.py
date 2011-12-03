'''
Created on 2 Dec 2011

mongo_utils

Loads Mongo DB with json versions of book bits
Provides utilities to clean up previous versions

Called after the pdf has been parsed and split

If you need MongoDB download, install and create the data/db folder
@author: Zak
'''

import pymongo
import os, os.path


class MongoClient():
    def __init__(self):
        pass
    
    def RemoveSmallMachines(self):
        '''
        Delete previous versions of small_machines
        '''
        pass
    
    def CreateSmallMachines(self):
        '''
        Create the indexes from small_machines
        '''
        pass
    
    def LoadSmallMachines(self):
        '''
        Load pages from small_machines
        '''
        pass
