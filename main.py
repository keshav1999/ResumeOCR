# Importing Python libraries
import numpy as np
import pandas as pd
from datetime import datetime

# Importing user defined functions
from Processes import ExtractText
from Processes import Findlist, FindReg, FindSec
from Processes import GetSections
from Processes import RefineMatches, ReplacePhrases
from Processes import listToString

def process_resume(filename):

    starttime = datetime.now()

    # extract_text(r'..//home/tanmay/Desktop/MyProjects/InvoiceOCR/Invoices/Invoice_Exp_Dec001_Veneklasen.pdf')
    # Code for reading doc or docx files to be added
    textstr = extract_text(filename)

    # Reading csv containing all master data related to fields
    xlsx = pd.ExcelFile('../Master_Data.xlsx')
    df = pd.read_excel(xlsx, 'Field_Match')
    
    # Get all section from the text
    all_sections = GetSections(textstr)

    # Reading index and text from passed string to extract each sentence
    for index,field_match in df.iterrows():

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


        #1	check if Section is present and section is part of all sections then get the filtered text for that section
        if field_match[8] != '' and all_sections.index(field_match[8]) != 0:
            next_section = all_sections[all_sections.index(field_match[8]) + 1]
            textsec = FindSec(textstr, field_match, next_section)
        else:
            textsec= textstr

        # 2	apply regex
        if field_match[2] != '':
            matches = listToString(FindReg(textsec, field_match))
        else:
            matches = textsec

        # 3	Filter Regex, skip values and Replace_Text
        if skip_values != '' or filter_regex != '':
            refine_match = replace_text(RefineMatches(matches, filter_regex, filter_values), replace_text)
        else:
            refine_match = matches
            
        # 4	filter on the specified list
        if field_match[7] != '':
            matchedvalues = Findlist(refine_match, field_match)

        #print csv  
        textstr.to_csv('Resume.csv')

        # Find Text
        Matchedvalues = find_text(textstr, filename)

        # #Print Matches Values
    
    
    print(Matchedvalues.dropna())

    endtime = datetime.now()
    diff = endtime - starttime

    print('Time taken: ' + str(diff.seconds))

# Calling the main function

process_resume('MAYANK Resume.pdf')