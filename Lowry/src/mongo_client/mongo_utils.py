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
from pymongo import Connection
from pymongo import database
import os, os.path
import simplejson as json
from text_analysis import pdf_parser
from pprint import pprint

HOST = "localhost"
MONGO_PORT = 27017
DATABASE = "small_machines"
COLLECTION = "pages"

FOLDER = "../../repository/small_machines/pdf_pages"

class MongoClient():
    def __init__(self):
        self.conn = Connection(HOST, MONGO_PORT)
        self.db = self.conn[DATABASE]
        self.mongo_collecton = self.db[COLLECTION]
        
        print("Created Database", self.db)
        print("Created collection", self.mongo_collecton)
        
    
    def RemoveSmallMachines(self):
        '''
        Delete previous versions of small_machines
        '''
        count = self.db[COLLECTION].count()
        print("Collection %s has %d documents" % (self.db[COLLECTION], count))
        self.db[COLLECTION].remove({})
    
    def CreateSmallMachines(self):
        '''
        Create the indexes from small_machines
        '''
        pass
    
    def LoadSmallMachinesTest(self):
        '''
        Load pages from small_machines
        '''
        
        page1 = {"page":"page1", "text":"a textual representation of page 1"}
        page2 = {"page":"page2", "text":"a textual representation of page 2"}
        page3 = {"page":"page3", "text":"a textual representation of page 3"}
    
        self.db.mongo_collection.save(page1)
        self.db.mongo_collection.save(page2)
        self.db.mongo_collection.save(page3)
        
        print "saved test pages"
        
    def LoadPagesFromFolder(self):
        parser = pdf_parser.PdfParser()
        files = list(parser.get_json_pages(FOLDER))   
        for f in files:
            data = self.read_json_file(os.path.join(FOLDER, f))
            self.db[COLLECTION].save(data)

    def read_json_file(self, filename):
        json_data = open(filename)
        return json.load(json_data)
        
    def ShowPages(self):
        cursor = self.db.mongo_collection.find()
        for page in cursor:
            print page    

    def ShowPage(self, index):
        page = self.db[COLLECTION].find_one({"page":"page_1"})
        if not type(page) == None:
            print(page)
            print(json.dumps((page["page"], page["content"])))

if __name__ == "__main__":
    mongo_client = MongoClient()
    
    mongo_client.RemoveSmallMachines()
    #mongo_client.LoadSmallMachinesTest()
    
    mongo_client.LoadPagesFromFolder()
    mongo_client.ShowPages()
    
    mongo_client.ShowPage(1)