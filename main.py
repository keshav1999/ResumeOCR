# Importing Python libraries
import numpy as np
import pandas as pd
from datetime import datetime

# Importing user defined functions
from Processes import extract_text
from Processes import find_text
from Processes import find_Abs


def process_resume(filename):

    starttime = datetime.now()

    # extract_text(r'..//home/tanmay/Desktop/MyProjects/InvoiceOCR/Invoices/Invoice_Exp_Dec001_Veneklasen.pdf')
    textstr = extract_text(filename)

    # Reading csv containing all master data related to fields
    xlsx = pd.ExcelFile('../Master_Data.xlsx')
    df = pd.read_excel(xlsx, 'Field_Match')
    
    # Reading index and text from passed string to extract each sentence
    for index,nu in df.iterrows():

        df_filter = df.

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