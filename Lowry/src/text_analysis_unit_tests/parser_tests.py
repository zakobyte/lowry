'''
Created on 30 Nov 2011

@author: Zak
'''
import unittest
from text_analysis import pdf_parser


class Test_PdfParser(unittest.TestCase):


    def setUp(self):
        self.pdf_parser = pdf_parser.PdfParser()
        
    def tearDown(self):
        self.pdf_parser = None
        


    def test_PdfParser(self):
        self.assertEquals(type(self.pdf_parser), pdf_parser.PdfParser)
    
    def test_NoPdfFile(self):
        pass
    
    def test_NoValidContent(self):
        pass
    
    def test_NoRootFolder(self):
        pass
    
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()