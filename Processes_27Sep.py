import invoice2data
from pytesseract import image_to_string, image_to_data, Output
from pdf2image import convert_from_path
import os
#import nltk
import numpy as np
import pandas as pd
from textblob import TextBlob
import re
from verbalexpressions import VerEx
import mysql.connector
from mysql.connector import errorcode
import math
import cv2
from PIL import Image

########################################################################################################################################
# Importing user functions
from PreProcessing import get_coord
from PreProcessing import preprocessing_image


# set path where invoice is
#os.chdir(r'//home/tanmay/Desktop/MyProjects/InvoiceOCR/Invoices')
os.chdir(r'/home/tanmay/Desktop/My Projects/InvoiceOCR/Invoices')

#########################################################################################################################################

# function to extract text
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

# Find mentioned fields values using mapping
def find_text(textstr, filename):

        # Reading csv containing all master data related to fields
        xlsx = pd.ExcelFile('../Master_Data.xlsx')
        df = pd.read_excel(xlsx, 'Field_Match')

        #Reading index and text from passed string to extract each sentence
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
                try:def extract_text
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
                except:
                        print('skipped')

        return(MatchedValues)

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
wdwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# Function to replace text
def replace_phrases(text, replace_text):

        final = True
        if str(replace_text) != '' :
                # Check filter text
                for phrase in replace_text.split('|'):
                        text = text.replace(phrase,'')

        return(text)

#########################################################################################################################################

# Reading items
def read_items(blob, filename):

        #Creating dataframe to store all matched values for first sentence according yto excel
        col_names=['Field','Sentence','Priority','Senlength']
        MatchedSen = pd.DataFrame(index=range(1,1000), columns=col_names)
        ind=0

        save_sen=''

        # Reading csv containing all master data related to fields
        xlsx = pd.ExcelFile('../Master_Data.xlsx')
        df = pd.read_excel(xlsx, 'For_Items')
        colpos = pd.read_excel(xlsx, 'colpos')

        for sentence in blob.sentences:

                for sen in sentence.split('\n'):

                        # Reading each tag
                        for index, row in df.iterrows():

                                #Assigning varibles from excel sheet
                                field = df.iloc[index,0]
                                use_recognize = df.iloc[index,7]
                                priority = df.iloc[index,5]

                                #Find keyword in sentence to find matching sentence sentence and find with highest priority
                                # 1 being highest priority
                                sen = sen.upper()
                                if use_recognize==1 and sen.find(field.upper()) != -1:

                                        MatchedSen.iloc[ind,0]=field
                                        MatchedSen.iloc[ind,1]=sen
                                        MatchedSen.iloc[ind,2]=priority
                                        MatchedSen.iloc[ind,3]=len(sen)
                                        ind =ind+1

        # Creating correct matrix for items
        save_sen = MatchedSen.sort_values(by=['Priority','Senlength'], ascending = False).iloc[0,1]
        Items = pd.DataFrame(index=range(1,100), columns=[colpos.iloc[:,0]])
        posofcol = pd.DataFrame(index = range(1,100), columns=['column', 'position','regex', 'filterregex','colpos','Field'])
        nav_words = save_sen.split(' ')

        print("First: " + save_sen)

        ind=0
        # Breaking first sentence to find sequence of columns
        for i in range(0,len(nav_words)):
                lvl=0

                for index, row in df.iterrows():
                        #Assigning varibles from excel sheet
                        field = df.iloc[index,0]
                        match = df.iloc[index,1]
                        regex = df.iloc[index,2]
                        filterregex = df.iloc[index,3]
                        pos = df.iloc[index,8]


                        try:

                                # Considering only 3 words will be matched each time
                                if len(field.split(' '))==1:
                                        testtext = nav_words[i]
                                        lvl = 1
                                if len(field.split(' '))==2 and i < len(nav_words)-1:
                                        testtext = nav_words[i] + ' ' + nav_words[i+1]
                                        lvl = 2
                                if len(field.split(' '))==3 and i < len(nav_words)-2:
                                        testtext = nav_words[i] + ' ' + nav_words[i+1] + ' ' + nav_words[i+2]
                                        lvl = 3
                                if len(field.split(' '))==4 and i < len(nav_words)-2:
                                        testtext = nav_words[i] + ' ' + nav_words[i+1] + ' ' + nav_words[i+2] + nav_words[i+3]
                                        lvl = 4
                        except Exception as e:
                                print(e)

                        # compare test string to find position of the text
                        if testtext.upper().find(field.upper()) != -1 :
                                # Increment i to skip read words
                                i = i+lvl-1
                                posofcol.iloc[ind,0] = match
                                posofcol.iloc[ind,1] = ind
                                posofcol.iloc[ind,2] = regex
                                posofcol.iloc[ind,3] = filterregex
                                posofcol.iloc[ind,4] = pos
                                posofcol.iloc[ind,5] = field
                                ind = ind + 1

        print(posofcol.dropna(how = 'all'))

        found_flag=0
        cntofsen = 0
        senlist=[]
        first_sen = 0

        # Reading lines after header found_flag
        for sentence in blob.sentences:

                for sen in sentence.split('\n'):
                        # checking if first sentence encountered
                        if found_flag>0 or sen.upper() == save_sen:
                                found_flag=found_flag + 1

                        # If first sentence found then find the rest of them
                        if found_flag>1:

                                pattern = re.compile('^[0-9]{1,2}[:.,-]?$')
                                matchflag = re.search(pattern, replace_phrases(sen.split(' ')[0], '}|{|/|\|<|>'))

                                # Capturing first sentence by default
                                if first_sen == 0:
                                        print(sen.upper())
                                        senlist.append(sen.upper())
                                        cntofsen = cntofsen + 1
                                        first_sen = 1
                                        continue

                                if matchflag:
                                        print(sen.upper())
                                        senlist.append(sen.upper())
                                        cntofsen = cntofsen + 1

                        # Break if 10 items read
                        if cntofsen == 10:
                                break

        # To read items lines we pass position of columns and list of item lines
        Items = read_item_lines(posofcol, senlist, Items, filename)

        return(Items)
 #########################################################################################################################################

# Function to read lines from items list based on first sentence
def read_item_lines(posofcol, itemlist, Items, filename):

        # Reading text with coordinates
        lst=[]
        i=0
        file, file_extension = os.path.splitext(filename)

        if file_extension=='.jpg' or file_extension=='.jpeg' or file_extension=='.png' :

                img = cv2.imread(filename)
                textdict = image_to_data(Image.fromarray(img), output_type=Output.DICT)

        if file_extension=='.pdf':
                pages = convert_from_path(filename)

                for page in pages:
                        page.save('out' +str(i)+'.jpg','JPEG')

                        #Converting file name to image array
                        img = cv2.imread('out' +str(i)+'.jpg')
                        textdict = image_to_data(Image.fromarray(img), output_type=Output.DICT)

        #Convert to upper case for all
        textdict['text'] = [i.upper() for i in textdict['text']]

        ind=0
        read=0
        matchflag = 0

        # Removing blanks and Sno as Sno is compulsory
        posofcol = posofcol.dropna(how = 'all')
        posofcol = posofcol[posofcol['column'] != 'Sno']

        
        # Finding top row for the items to filter out initial rows as names can be repeated and 
        # it fudges the result when trying to find the left coordinate below
        top =0
        for i,row in posofcol.iterrows():
                temptop = textdict['text'].index(str(row[5]).split(' ')[0].upper())
                if temptop>top : top = temptop
        
        #Filter out records till header of items
        lstleft=[]
        lsttext=[]
        ind=0
        i=0
        for k in textdict['top']:
                if k > top:
                        lstleft.append(textdict['left'][i])
                        lsttext.append(textdict['text'][i])
                        i=i+1

        textfil={}
        textfil['left'] = lstleft
        textfil['text'] = lsttext

        textdict = textfil

        posofcol_bkp = posofcol
        #try:
        # Reading each item
        for sen in itemlist:

                posofcol = posofcol_bkp
                for word in sen.split(' '):


                        # Flag to check if already a near word found then append the current text
                        append_on_same = 0 
                        
                        # Comparing left column position of each word with  left column position headers columns to align the text
                        for i, row in posofcol.iterrows():
                                matchflag=0

                                # Finding index position using text
                                index = textdict['text'].index(str(posofcol.iloc[i-2,5]).split(' ')[0].upper())
                                index_word = textdict['text'].index(word.upper())

                                #Using Index to find the columnar position
                                colpos = textdict['left'][index]
                                colpos_word = textdict['left'][index_word]

                                if  abs(colpos - colpos_word)<=50:
                                        matchflag = 1

                                # pattern = re.compile(row[2])
                                # matchflag = re.search(pattern, word)

                                if matchflag==1:
                                        # Setting Sno by default
                                        Items.iloc[ind, 0] = ind+1
                                        if append_on_same == 0:
                                                Items.iloc[ind, row[4]-1] = word
                                        else:
                                                Items.iloc[ind, row[4]-1].append(word)
                                        #posofcol = posofcol.drop(posofcol.index[i-2])
                                        break

                ind = ind + 1
        # except Exception as e:
        #         print('check' + str(e))
        print(posofcol_bkp)
        print(Items.dropna(how = 'all'))
        return(Items)

#########################################################################################################################################

# Function to refine reading of items
def refine_items(Items):
        # Reading csv containing all master data related to fields
        xlsx = pd.ExcelFile('../Master_Data.xlsx')
        colpos = pd.read_excel(xlsx, 'colpos')

        for i in range(0,len(colpos)):
                print('to be written')

        return
#########################################################################################################################################

# Function to convert text to int/float
def cast_values(x):
        try:
                y = float(x)
        except:
                print(x)
                y=0
        return(y)

#########################################################################################################################################