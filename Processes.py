from pytesseract import image_to_string, image_to_data, Output
from pdf2image import convert_from_path
import os
#import nltk
import numpy as np
import pandas as pd
from textblob import TextBlob
import re
from verbalexpressions import VerEx
from pathlib import Path
import cv2
from PIL import Image
import math

# Functions to filter out the required text:
# 1. FindReg - Just use regex to filter
# 2. FindList - Use the regex and grammar to search if regex specified and
#               Use the mentioned file to pick the specified names
# 3. FindSec - Filter the text string for the specified section 
# 4. 
# 5. GetSections - To get all the sections present in the resume
# 6. Extract data from image or pdfs

#########################################################################################################################################
# 1. FindAbs - Just use regex to filter
# Find mentioned fields values using mapping

def FindReg(textstr, field_match):

    Pattern = re.compile(field_match[2])
    matches = Pattern.findall(textstr)
    
    print(matches)
    return(matches)

#########################################################################################################################################

# 2. FindList - Use the regex and grammar to search if regex specified and
#               Use the mentioned file to pick the specified names

def Findlist(textstr, field_match, matches):

    # Reading file to match the master value list
    file_name = field_match[7]
    mas_list = pd.read_csv(file_name)

    # Declaring variables to store final results    
    ind = 0
    col_names=['Field','Match_Field','text']
    MatchedValues = pd.DataFrame(index=range(1,1000), columns=col_names)

    # if regex is present
    if len(matches) != '':
        
        #comparing matched values against the read master values
        for i in matches:

            match_master = mas_list.loc[mas_list['Values'] == i]

            if len(match_master) != 0:

                MatchedValues.iloc[ind,0]= field_match[0]
                MatchedValues.iloc[ind,1]= field_match[1]
                MatchedValues.iloc[ind,2] = i
    else:
        
        for i in mas_list['Values']:
            
            loc = textstr.find(i)

            if loc>0:
            
                MatchedValues.iloc[ind,0]= field_match[0]
                MatchedValues.iloc[ind,1]= field_match[1]
                MatchedValues.iloc[ind,2] = i

    print(MatchedValues)
    return(MatchedValues)

#########################################################################################################################################

# 3. FindSec - it will filter the text for a particular section
def FindSec(textstr, field_match, next_section):

    # pick the section to be filtered
    section = field_match[8]

    # extract words
    blob = blob(textstr)
    extracted_text =''

    section_found = 0

    for i in range(0,len(blob.words)):

        if (blob.words[i] == section) or (blob.words[i] + ' ' + blob.words[i+1] == section) or (blob.words[i] + ' ' + blob.words[i+1] + ' ' + blob.words[i+2] == section) :
            section_found=1
        
        if section_found == 1:

            if (blob.words[i] == next_section) or (blob.words[i] + ' ' + blob.words[i+1] == next_section) or (blob.words[i] + ' ' + blob.words[i+1] + ' ' + blob.words[i+2] == next_section) :

                extracted_text = extracted_text + blob.words[i] + ' '

    return()

#########################################################################################################################################

# 5. To get all the sections present in the resume

def GetSections(textstr,section):
    
    # Finding sections in the resume
    xlsx = pd.ExcelFile('../Master_Data.xlsx')
    sec = pd.read_excel(xlsx, 'Sections')
    
    all_sections = []
    ind=0

    # Filtering the sections
    for i in sec['Keywords']:
        
        loc = textstr.find(i)

        if loc>0:
            all_sections[ind]=i
            ind=ind+1

    return(all_sections)

#########################################################################################################################################
# 6. to extract text from image or pdfs

def extract_text(filename):

        i=0
        lst = []
        # Getting file extension
        file, file_extension = os.path.splitext(filename)

        if file_extension=='.jpg' or file_extension=='.jpeg' or file_extension=='.png' :

                #Converting file name to image array
                img = cv2.imread(filename)
                #img_processed = preprocessing_image(img)

                text = image_to_string(Image.fromarray(img))
                lst.append(text)

        if file_extension=='.pdf':
                pages = convert_from_path(filename)

                for page in pages:
                        page.save('out' +str(i)+'.jpg','JPEG')

                        #Converting file name to image array
                        img = cv2.imread('out' +str(i)+'.jpg')
                        #img_processed = preprocessing_image(img)

                        text = image_to_string(Image.fromarray(img))
                        lst.append(text)
                        i=i+1

        textstr = pd.Series(lst)
        return(textstr)

#########################################################################################################################################
