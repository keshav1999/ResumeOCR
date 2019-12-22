# Importing Python libraries
import numpy as np
import pandas as pd
from datetime import datetime
import os
from textblob import TextBlob
import math

# Importing user defined functions
from Processes import ExtractText
from Processes import Findlist, FindReg, FindSec
from Processes import GetSections
from Processes import Find_Values
from Processes import RefineMatches, ReplacePhrases
from Processes import listToString
from Processes import extractName
from Processes import Filter_values


os.chdir(r'/home/tanmay/Desktop/My Projects/ResumeOCRfile/Resume')
def process_resume(filename):
    starttime = datetime.now()
    name = filename
    names = name.split('.')
    
    # Code for reading doc or docx files to be added
    textstr,text = ExtractText(filename)
    
    # Reading csv containing all master data related to fields
    xlsx = pd.ExcelFile('../Master_Data.xlsx')
    df = pd.read_excel(xlsx, 'Field_Match')
    
    # Get all section from the text
    all_sections = GetSections(textstr)
    print(all_sections)
    Matchedvaluesdf = pd.DataFrame()
    
    # Reading index and text from passed string to extract each sentence
    for index,field_match in df.iterrows():
        print(field_match)
        print(df.iloc[index,2])
        print(df.iloc[index,7])
        x= 0
        # Setting filter regex
        try:
                if math.isnan(df.iloc[index,1]) == False:
                        nationality = df.iloc[index,1]
                else: nationality="Indian"
        except: nationality = df.iloc[index,1]

        try:
                if math.isnan(df.iloc[index,3]) == False:
                        filter_regex = df.iloc[index,3]
                else: filter_regex=''
        except: filter_regex = df.iloc[index,3]
        # Setting filter valuesrrows():
        # Setting filter regex
        try:
                if math.isnan(df.iloc[index,7]) == False:
                        sheet_name = df.iloc[index,7]
                else: sheet_name=''
        except: sheet_name = df.iloc[index,7]
        if sheet_name != '':
                Matchedvaluessheet = Find_Values(sheet_name,textstr)
                x = 1
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
        # Matchedvalueslist = []
        print(field_match[8])
        #1	check if Section is present and section is part of all sections then get the filtered text for that section
        if field_match[8] != '' and len(all_sections[all_sections == field_match[8]]) != 0:
                x = 1
                a=list(all_sections)
                index_no = a.index(field_match[8])
                next_section = all_sections[index_no]
                textsec = FindSec(text, field_match, next_section)
                if next_section == "PERSONAL DETAILS":
                        try:
                                if math.isnan(df.iloc[index,7]) == False:
                                        sheet_name = df.iloc[index,7]
                                else: sheet_name=''
                        except: sheet_name = df.iloc[index,7]
                        if sheet_name != '':
                                Matchedvaluessheet = Find_Values(sheet_name,textstr)
                                x = 1
                                break
        #     textsec = list(textsec)
                ##print(textsec)
                col_names=['Field','Match_Field','text','loc']
                # col_names=['Field','Match_Field','text']
                
                ind = 0
                Matchedvaluessheet = pd.DataFrame(index=range(1,1000), columns=col_names)
                Matchedvaluessheet.iloc[ind,0]= 'Field'
                Matchedvaluessheet.iloc[ind,1]=  next_section
                Matchedvaluessheet.iloc[ind,2] = textsec    
                Matchedvaluessheet.iloc[ind,3] = "loc"      
        else:
                textsec = listToString(textstr)
                try:
                        if math.isnan(field_match[2]) == False:
                                matches = listToString(FindReg(textsec, field_match))
                        else: matches = textsec
                except: matches = listToString(FindReg(textsec, field_match))
                if skip_values != '' or filter_regex != '':
                        refine_match = replace_text(RefineMatches(matches, filter_regex, skip_values), replace_text)
                else:
                        refine_match = matches
                
                # 4	filter on the specified list
                try:
                        if math.isnan(field_match[2]) == False:
                                Matchedvalues = Findlist(refine_match, field_match)
                        else:
                                if nationality == "Indian":
                                        col_names=['Field','Match_Field','text','loc']
                                        ind = 0
                                        MatchedValues = pd.DataFrame(index=range(1,1000), columns=col_names)
                                        MatchedValues.iloc[ind,0]= 'Find'
                                        MatchedValues.iloc[ind,1]= 'Field'
                                        MatchedValues.iloc[ind,2] = 'Indian'
                                        MatchedValues.iloc[ind,3] = ''
                                else:
                                        col_names=['Field','Match_Field','text','loc']
                                        ind = 0
                                        MatchedValues = pd.DataFrame(index=range(1,1000), columns=col_names)
                                        MatchedValues.iloc[ind,0]= 'Find'
                                        MatchedValues.iloc[ind,1]= 'Field'
                                        MatchedValues.iloc[ind,2] = ''    
                                        MatchedValues.iloc[ind,3] = ''                            
                except: 
                        Matchedvalues = Findlist(refine_match, field_match)
                textstr.to_csv('Resume.csv')
        if x == 1:
            Matchedvaluesdf = Matchedvaluesdf.append(Matchedvaluessheet)    
            print(Matchedvaluesdf.dropna())
        else:
            Matchedvaluesdf = Matchedvaluesdf.append(Matchedvalues)
            print(Matchedvaluesdf.dropna())
    
        # Calling Extract Name function
        MatchedValuesName = extractName(filename)
        print(MatchedValuesName)
        Matchedvaluesdf.append(MatchedValuesName)
        print(Matchedvaluesdf)
        # Remove duplicate values
        Matchedvalues = Filter_values(Matchedvalues)

        print(Matchedvaluesdf.dropna())
        endtime = datetime.now()
        diff = endtime - starttime

        print('Time taken: ' + str(diff.seconds))

# Calling the main function
process_resume('BhawnaMudgal[2_2].pdf')