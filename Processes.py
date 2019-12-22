from pytesseract import image_to_string, image_to_data, Output
from pdf2image import convert_from_path
import os
import sys
import numpy as np
import pandas as pd
from textblob import TextBlob
import pytesseract
import re
from verbalexpressions import VerEx
from pathlib import Path
import cv2
from PIL import Image
import subprocess
from subprocess import  Popen
import math
import xlwt 
from xlwt import Workbook
import nltk
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
# Functions to filter out the required text:
# 1. FindReg - Just use regex to filter
# 2. FindList - Use the regex and grammar to search if regex specified and
#               Use the mentioned file to pick the specified names
# 3. FindSec - Filter the text string for the specified section 
# 4. 
# 5. GetSections - To get all the sections present in the resume
# 6. ExtractText - Extract data from image or pdfs
# 7. RefineMatches - function to refine multiple regex matches and values
# 8. ReplacePhrases - Function to replace text
# 9. listToString - Function to convert   
# 10. find_next_section - Use to find where from next section start
# 11. extractName - Use file name or any string and extract name from it
# 12. Filter_Values - Remove duplicates from dataframe
# 13. define_nationality - Pick nationality or be default

#########################################################################################################################################
# 1. FindAbs - Just use regex to filter
# Find mentioned fields values using mapping

def FindReg(textstr, field_match):
    Pattern = re.compile(field_match[2])
    matches = Pattern.findall(textstr)
    return(matches)

#########################################################################################################################################

# 2. FindList - Use the mentioned file to pick the specified names

def Findlist(textstr, field_match):
    # Reading file to match the master value list
    file_name = field_match[7]
    try:
                if math.isnan(file_name) == True:
                        col_names=['Field','Match_Field','text','loc']
                        ind = 0
                        MatchedValues = pd.DataFrame(index=range(1,1000), columns=col_names)
                        MatchedValues.iloc[ind,0]= field_match[0]
                        MatchedValues.iloc[ind,1]= field_match[1]
                        MatchedValues.iloc[ind,2] = textstr
                        MatchedValues.iloc[ind,3] = ""
                        context[field_match[1]] = textstr
                else: 
                        xlsx = pd.ExcelFile('../Master_Data.xlsx')
                        mas_list = pd.read_excel(xlsx, file_name)  
                        ind = 0
                        col_names=['Field','Match_Field','text','loc']
                        MatchedValues = pd.DataFrame(index=range(1,1000), columns=col_names)
                                
                        for i in mas_list['Values']:
                                
                                loc = textstr.find(i)

                                if loc>0:
                                
                                        MatchedValues.iloc[ind,0]= field_match[0]
                                        MatchedValues.iloc[ind,1]= field_match[1]
                                        MatchedValues.iloc[ind,2] = i
                                        MatchedValues.iloc[ind,3] = ""
    except: 
                col_names=['Field','Match_Field','text','loc']
                ind = 0
                MatchedValues = pd.DataFrame(index=range(1,1000), columns=col_names)
                MatchedValues.iloc[ind,0]= field_match[0]
                MatchedValues.iloc[ind,1]= field_match[1]
                MatchedValues.iloc[ind,2] = textstr 
                MatchedValues.iloc[ind,3] = ""
    return(MatchedValues)

#########################################################################################################################################

# 3. FindSec - it will filter the text for a particular section
def FindSec(textstr, field_match, next_section):
    section = field_match[8]
    i=0
    # extract words
    textstr = str(textstr)
    blob = TextBlob(textstr)
    extracted_text =''
    section_found = 0
    count = 0
    for i in range(0,len(blob.words)-1):
        if ((blob.words[i].upper() == section.upper()) or (blob.words[i].upper() + ' ' + blob.words[i+1].upper() == section.upper())) :
           if ((blob.words[i].upper() + ' ' + blob.words[i+1].upper() == section.upper())):
               section_found=1   
               continue
           else:
               section_found=2
        elif section_found == 2 or section_found == 1: 
            count = count + 1
            if (blob.words[i].upper() == next_section.upper()) or (blob.words[i].upper() + ' ' + blob.words[i+1].upper() == next_section.upper()) or (blob.words[i].upper() + ' ' + blob.words[i+1].upper()) :
                if count != 1:
                        value = find_next_section(blob.words[i].upper())
                        if value == 0 or value == "experience":
                                extracted_text = extracted_text + blob.words[i] + ' '
                        else:
                                break
    print(extracted_text)    
    return(extracted_text)

#########################################################################################################################################

# 5. To get all the sections present in the resume

def GetSections(textstr):
    
    # Finding sections in the resume
    xlsx = pd.ExcelFile('../Master_Data.xlsx')
    sec = pd.read_excel(xlsx, 'Sections')
    all_sections = []
    ind=0
#     wb = Workbook() 
#     sheet1 = wb.add_sheet("New")
    
    # Filtering the sections
    j = 0
    for i in sec['Keyword']:   
        
        loc = listToString(textstr).upper().find(i.upper())
        
        ind = 0
        if loc>0:
            all_sections.append(sec['Section'][j])
        
        #     sheet1.write(ind, 0, i) 
            ind=ind+1   
        j = j + 1
#     wb.save("Master_Data.xlsx") 
    return(pd.Series(all_sections))
#########################################################################################################################################
# 6. to extract text from image or pdfs

def ExtractText(filename):
        path = os.chdir(r'/home/tanmay/Desktop/My Projects/ResumeOCRfile/Resume')
        image_to_string_text = ""
        i=0
        lst = []
        # Getting file extension
        file, file_extension = os.path.splitext(filename)
        
        wdFormatPDF = 17
        
        if file_extension=='.jpg' or file_extension=='.jpeg' or file_extension=='.png' :

                #Converting file name to image array
                img = cv2.imread(filename)
                text = image_to_string(Image.fromarray(img))
                image_to_string_text = image_to_string_text + text
                lst.append(text)
        if file_extension=='.doc'or file_extension=='.docx':
                cmd = 'libreoffice --convert-to pdf'.split() + [filename]
                
                p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                
                p.wait(timeout=10)
                stdout, stderr = p.communicate()
                
                if stderr:
                        raise subprocess.SubprocessError(stderr)
                file_extension = '.pdf'
                filename = file+'.pdf'
                
        if file_extension=='.pdf':
                pages = convert_from_path(filename)
                for page in pages:
                        page.save('out' +str(i)+'.jpg','JPEG')

                        #Converting file name to image array
                        img = cv2.imread('out' +str(i)+'.jpg')
                        text = image_to_string(Image.fromarray(img))
                        blob = TextBlob(text)
                        data = pytesseract.image_to_string(img, output_type=Output.DICT)
                        image_to_string_text = image_to_string_text + text
                        lst.append(text)
                        i=i+1
        textstr = pd.Series(lst)
        return(textstr,image_to_string_text)
#########################################################################################################################################
# 7. function to refine multiple regex matches and values
# True  - means none of the filters matched
# False - means filter applied and not to be considered
def RefineMatches(text, filter_regex, filter_values):

        skip = True
        if str(filter_values) != '' :
                # Check filter text
                for filter in filter_values.split('|'):
                        if text == filter:
                                skip = False
        # Check filter regex
        if str(filter_regex) != '' :
                for regex in filter_regex.split('|'):
                        pattern = re.compile(regex)
                        matchflag = re.search(pattern, text)
                        if matchflag:
                                skip = False
        return(skip)
#########################################################################################################################################
# 8. Function to replace text
def ReplacePhrases(text, replace_text):

        final = True
        if str(replace_text) != '' :
                # Check filter text
                for phrase in replace_text.split('|'):
                        text = text.replace(phrase,'')

        return(text)

#########################################################################################################################################

# 9. listToString - Function to convert   
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 = str1 + ele + ' '
    # return string   
    return str1  

#########################################################################################################################################

# 10. find_next_section - Use to find where from next section start
 
def find_next_section(text):
        
        xlsx = pd.ExcelFile('../Master_Data.xlsx')
        df = pd.read_excel(xlsx, 'Sections')
        end_of_process = 0
        for index, row in df.iterrows():
                        # fuzz.partial_ratio(df.iloc[index,0].upper(),text)
                        # if fuzz.partial_ratio(df.iloc[index,0].upper(),text) >= 100:
                        #         if len(text) >= 4:
                        #                 end_of_process = df.iloc[index,0]
                        if (df.iloc[index,0].upper() == text):
                                end_of_process = df.iloc[index,0]
                                break
        if text == "EXPERIENCE" or text == "SKILLS":
                end_of_process = 0
        if end_of_process == 0:
                return(end_of_process)
        else: 
                end_of_process = 1
                return(end_of_process)


def Find_Values(section,textstr):
        
        count = 1
        section = section.upper()
        xlsx = pd.ExcelFile('../Master_Data.xlsx')
        sec = pd.read_excel(xlsx, section)
        
        all_sections = []
#     wb = Workbook() 
#     sheet1 = wb.add_sheet("New")
        ind = 0
        col_names=['Field','Match_Field','text','loc']
        MatchedValuesnew = pd.DataFrame()
        MatchedValues = pd.DataFrame(index=range(1,1000), columns=col_names)
        for i in sec['Keyword']:        
                loc = listToString(textstr).upper().find(i.upper())
        
                if loc>0: 
                        if section == "NAMES":
                              if loc <= 100:
                                        all_sections.append(i)
        
                                        #     sheet1.write(ind, 0, i) 
                                        
                                        
                                        MatchedValues.iloc[ind,0]= section
                                        MatchedValues.iloc[ind,1]= count
                                        MatchedValues.iloc[ind,2] = i
                                        MatchedValues.iloc[ind,3] = loc
                                        count = count + 1
                                        MatchedValuesnew = MatchedValuesnew.append(MatchedValues)
        
                        else:
                                        all_sections.append(i)
        
                                        #     sheet1.write(ind, 0, i) 
                                        
                                        
                                        MatchedValues.iloc[ind,0]= section
                                        MatchedValues.iloc[ind,1]= count
                                        MatchedValues.iloc[ind,2] = i
                                        MatchedValues.iloc[ind,3] = loc
                                        count = count + 1
                                        MatchedValuesnew = MatchedValuesnew.append(MatchedValues)
        
                                        if i == "Female":
                                                break
        
        return(MatchedValuesnew.dropna())


#########################################################################################################################################        
# 11. extractName - Use file name or any string and extract name from it

def extractName(filename):

        #removing extension
        filestr = os.path.splitext(filename)[0]

        filemod =""
        for x in filestr:
                # To check if name is in Capital
                if filestr[0].isupper() and filestr[1].isupper():
                        filemod = filestr
                        break
                
                # To Split first and last name where no spaces
                if x.isupper() and x != filestr[0] :
                        filemod = filemod + " "
                filemod = filemod + x

        #Replacing common keywords CV/Resume/Profile
        filestr =  filemod.upper().replace("CV","")
        filestr =  filestr.upper().replace("RESUME","")
        filestr =  filestr.upper().replace("PROFILE","")
        filestr =  filestr.upper().replace("_"," ")

        # Filtering out only text/characters
        name = re.sub('[^a-z A-Z]+', '', filestr)

        # Extract parts of name
        namelist = list(filter(None,re.split(" ", name)))
        firstname = namelist[0]
        if namelist[0] != namelist[-1] :        
                lastname  = namelist[-1]
                middlename = namelist[1:-1]

        col_names=['Field','Match_Field','text','loc']
        MatchedValues = pd.DataFrame(index=range(1,4), columns=col_names)        
        
        # Add to Matched values
        try:
                MatchedValues.iloc[0,0]= "First Name"
                MatchedValues.iloc[0,1]= "First Name"
                MatchedValues.iloc[0,2] = firstname
                MatchedValues.iloc[0,3] = ""

                MatchedValues.iloc[1,0]= "Middle Name"
                MatchedValues.iloc[1,1]= "Middle Name"
                MatchedValues.iloc[1,2] = ''.join(middlename)
                MatchedValues.iloc[1,3] = ""

                MatchedValues.iloc[2,0]= "Last Name"
                MatchedValues.iloc[2,1]= "Last Name"
                MatchedValues.iloc[2,2] = lastname
                MatchedValues.iloc[2,3] = ""
        except: 
              MatchedValues = MatchedValues

        return MatchedValues

#########################################################################################################################################        
# 12. Filter_Values - Remove duplicates from dataframe

def Filter_values(before_refine):
        before_refine = before_refine.sort_values('text', ascending=False).drop_duplicates(['Match_Field'])    
        return(before_refine)

#########################################################################################################################################        
# 13. define_nationality - Pick nationality or be default

def define_nationality(MatchedValues):
        pass

