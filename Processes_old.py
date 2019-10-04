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

########################################################################################################################################
# Importing user functions
# from PreProcessing import get_coord
# from PreProcessing import preprocessing_image

# set path where invoice is
#os.chdir(r'//home/tanmay/Desktop/MyProjects/InvoiceOCR/Invoices')
os.chdir(r'/home/tanmay/Desktop/My Projects/ResumeOCR/Resume')

#########################################################################################################################################

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

#########################################################################################################################################

# Finding text based on following types:
# 1. FindAbs - Just use regex to filter
# 2. FindList - Use the regex and grammar to search if regex specified and
#               Use the mentioned file to pick the specified names
# 3. NLTK - Use the regex and grammar to search
# 4. None of the above - Search for the keyword and use text after it using Regex


# Find mentioned fields values using mapping
def find_text(textstr, filename):

        # Reading csv containing all master data related to fields
        xlsx = pd.ExcelFile('../Master_Data.xlsx')
        df = pd.read_excel(xlsx, 'Field_Match')
        df_key = pd.read_excel(xlsx, 'Sections')

        # Reading index and text from passed string to extract each sentence
        for txt,text in textstr.iteritems():
                
                #Printing Name
                print("Name of the candidate: ")
                if len(text.split('\n')[0])>2:
                        print(text.split('\n')[0])
                elif len(text.split('\n')[1])>2:
                        print(text.split('\n')[1])
                
                for index,nu in df.iterrows():
                        
                        field = df.iloc[index,0]
                        Match = df.iloc[index,1]
                        regex = df.iloc[index,2]

                        if field == 'FindAbs':
                                Pattern = re.compile(regex)
                                matches = Pattern.findall(text)
                                print(matches)

                #Printing blocks from resume
                #for i in df_key.iterrows():
                        

        # Reading index and text from passed string to extract each sentence
        for txt,text in textstr.iteritems():
                # Creating textblob to traverse through words
                blob = TextBlob(text)

                # Calling read items to return items list
                #read_items(blob, filename)

                ind = 0
                col_names=['Field','Match_Field','text']
                MatchedValues = pd.DataFrame(index=range(1,1000), columns=col_names)
                pos=0
                word=''

                #Iterating through each word in the blob
                #try:
                for word in blob.words:

                        # Iterating through each row in master data rules
                        for index, row in df.iterrows():

                                #Assigning varibles from excel sheet

                                field = df.iloc[index,0]
                                Match = df.iloc[index,1]
                                regex = df.iloc[index,2]

                                priority = df.iloc[index,5]

                                # Setting filter regex
                                try:
                                        if math.isnan(df.iloc[index,3]) == False:
                                                filter_regex = df.iloc[index,3]
                                        else: filter_regex=''
                                except: filter_regex = df.iloc[index,3]

                                # Setting filter values
                                try:
                                        if math.isnan(df.iloc[index,6]) == False:
                                                skip_values = df.iloc[index,6]
                                        else: skip_values=''
                                except: skip_values = df.iloc[index,6]

                                # Setting replace text
                                try:
                                        if math.isnan(df.iloc[index,4]) == False:
                                                replace_text = df.iloc[index,4]
                                        else: replace_text=''
                                except: replace_text = df.iloc[index,4]

                                skip=True

                                matchtext=''
                                txtlen = len(field.split())

                                # Creating text as per the length of field to be compared
                                for i in range(0,txtlen):
                                        if i > 0:
                                                matchtext = matchtext + ' '
                                        matchtext = matchtext + blob.words[pos+i].upper()
                                
                                if (matchtext==field.upper()):

                                        pattern = re.compile(regex)
                                        for SubIndex in range(0,2):
                                                matchflag = re.search(pattern, blob.words[pos+txtlen+SubIndex])

                                                # Replacing phrases to clean the text
                                                after_replace_text =  replace_phrases(blob.words[pos+txtlen+SubIndex], replace_text)

                                                # Filtering text based on regex and values
                                                skip = refine_matches(after_replace_text, filter_regex, skip_values)
                                                if matchflag and skip:
                                                        break

                                        # If perfect match then save the entry
                                        if matchflag:
                                                MatchedValues.iloc[ind,0]=field
                                                MatchedValues.iloc[ind,1]=Match
                                                MatchedValues.iloc[ind,2]= after_replace_text
                                                ind = ind + 1

                        pos = pos + 1
                #except:
                #        print('skipped')

        return(MatchedValues)

#########################################################################################################################################

#########################################################################################################################################

#function to refine multiple regex matches and values
# True  - means none of the filters matched
# False - means filter applied and not to be considered
def refine_matches(text,filter_regex, filter_values):

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
# Function to replace text
def replace_phrases(text, replace_text):

        final = True
        if str(replace_text) != '' and replace_text != None:
                # Check filter text
                for phrase in replace_text.split('|'):
                        text = text.replace(phrase,'')

        return(text)

#########################################################################################################################################

