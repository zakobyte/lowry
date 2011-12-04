'''
Created on 24 Nov 2011

Provide functions to parse pdfs to be used in search and analysis


@author: Zak
'''

# import section - if you do not have package references use easy_install in c:\PythonFolder\Scripts
# then add a reference to the installed egg or folder in Window\Perferences\
import os, os.path      # Probably refactor this out to a utility file later
import pyPdf            # Pdf functions out the box. 
import nltk             # Natural Language Toolkit
import unicodedata      # Useful to format text when writing to file
import json             # Used to dump json versions of the pages
import fnmatch          # simple mathc utility used in file finding

class PdfParser():
    def __init__(self):
        pass
    
    def check_file_exists(self, filename):
        '''
        Belt and braces approach to file usage as check is also run under main opening functions
        '''
        try:
            open(filename)
            return True
        except:
            return False
        
    def check_folder_exists(self, foldername):
        '''
        Check if a folder exists - used to remove contents as required 
        '''
        return os.path.isdir(foldername)
        
    def pdf_to_pages(self, folder, file):
        '''
        Converts a pdf file to separate pages in pdf format
        '''
        pdf_filename = os.path.join(folder, file)
        
        if self.check_file_exists(pdf_filename):
            try:
                folder_out = os.path.join(folder, "pdf_pages")
                
                if not self.check_folder_exists(folder_out):
                    os.mkdir(folder_out)
                    
                print "Reading"
                pdf_reader = pyPdf.PdfFileReader(open(pdf_filename, "rb"))
                
                num_pages = pdf_reader.getNumPages()
                
                i = 0
                while i < num_pages:
                    i += 1
                    file_out = os.path.join(folder, "pdf_pages" , "small_machines_page_" + str(i) + ".pdf")
                    fw_out = pyPdf.PdfFileWriter()
                    fw_out.addPage(pdf_reader.getPage(i - 1))
                    
                    out_stream = open(file_out, "wb")
                    fw_out.write(out_stream)
                    out_stream.close()      
            
            except Exception as e:
                print("({})".format(e))
    
    def pdf_to_text(self, folder, file):
        '''
        Converts pdfs to plain text
        '''
        pdf_filename = os.path.join(folder, file)
        
        if self.check_file_exists(pdf_filename)  == True: 
            try:
                print "Reading"
                pdf_reader = pyPdf.PdfFileReader(open(pdf_filename, "rb"))
                
                print "Converting"
                text_content = self.convert_pdf_to_text(pdf_reader)
    
                print "Writing"
                text_filename = pdf_filename.replace(".pdf", ".txt")        
                self.write_text(text_filename, text_content)
            
            except Exception as e:
                print("({})".format(e))   
        else:
            print("file ", pdf_filename, " does not exist")
        
            
    def convert_pdf_to_text(self, pdf_content): 
        '''
        convert_pdf_to_text
        Accept a PdfFilreReader and return a string of text
        '''           
        pages = [] # empty list
        text_content = ""
        
        num_pages = pdf_content.getNumPages()
        for i in range(0, num_pages):
            # Extract text from page and add to content
            content = pdf_content.getPage(i).extractText() + "\n"
            content = unicodedata.normalize('NFKD', content).encode('ascii','ignore')
            #print content
            pages.append(content)
            text_content += content
        
        return text_content

    def convert_pdfpages_to_json(self, pdf_foldername):
        '''
        Reads a folder for pdf files using the handy walk function
        For each pdf file found it creates a .json equivalent
        
        Note use of pattern to exclude previously converted files
        '''
        
        print("Reading folder for pages: ", pdf_foldername)
        for path, subdirs, files in os.walk(pdf_foldername):
            pattern = "*.pdf"
            files.sort()
            page_num = 1
            for name in files:
                if (fnmatch.fnmatch(name, pattern)):
                    self.convert_pdfpage_to_json(os.path.join(path, name), page_num)
                    page_num += 1
        
    def convert_pdfpage_to_json(self, pdf_filename, page_num):
        '''
        Make json representations of each file
        They will be loaded into the databases and used for searching using RESTful queries
        '''
        
        print("starting conversion to json: ", pdf_filename)
        json_filename = pdf_filename.replace(".pdf", ".json")
        
        fr_pdf = pyPdf.PdfFileReader(open(pdf_filename, "rb"))
        
        text = self.convert_pdf_to_text(fr_pdf)
        
        json_data = {'page_num': page_num, 'page':'page_' + str(page_num),'name':pdf_filename, 'content':text}
        
        json_file = open(json_filename, "wb")
        json.dump(json_data, json_file)
        json_file.close()
        
    def get_json_pages(self, json_foldername):
        for path, subdirs, files in os.walk(json_foldername):
            pattern = "*.json"
            #files.sort()
            json_files = []
            for name in files:
                if (fnmatch.fnmatch(name, pattern)):
                    json_files.append(name)
        
        return json_files
            
    def write_text(self, text_filename, text_content):
        '''
        If the file exists overwrite it
        '''
        try:
            f = open(text_filename, "w")
            f.write(text_content)
            f.close()
        except Exception as e:    
            print("({})".format(e))
            
    
if __name__ == "__main__":
    '''
    Allows the interpreter determine to run this as the main programme or if it called from another one
    '''
    root_folder = "../../repository/small_machines"
    document_name = "Small_Machines.pdf"
    
    pdf_parser = PdfParser()
    
    pdf_parser.pdf_to_text(root_folder, document_name)
    
    pdf_parser.pdf_to_pages(root_folder, document_name)
    
    folder_pages = os.path.join(root_folder, "pdf_pages")
    
    pdf_parser.convert_pdfpages_to_json(folder_pages)
    
    
