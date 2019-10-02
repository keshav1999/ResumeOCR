# Importing Python libraries
import numpy as np
import pandas as pd
from datetime import datetime

# Importing user defined functions
from Processes import extract_text
from Processes import find_text
from Processes import refine_matches

def process_invoice(filename):

    starttime = datetime.now()

    # extract_text(r'..//home/tanmay/Desktop/MyProjects/InvoiceOCR/Invoices/Invoice_Exp_Dec001_Veneklasen.pdf')
    textstr = extract_text(filename)

    #print csv  
    textstr.to_csv('InvoiceText.csv')

    # Find Text
    Matchedvalues = find_text(textstr, filename)

    #Print Matches Values
    print(Matchedvalues.dropna())

    endtime = datetime.now()
    diff = endtime - starttime

    print('Time taken: ' + str(diff.seconds))

# Calling the main function

#process_invoice('Audit Fee.pdf')
#process_invoice('Sale Invoice 1.pdf')
#process_invoice('Invoice_Exp_Dec001_Veneklasen.pdf')
process_invoice('finsq_invoice.jpg')

#refine_matches('18','','5|12|18')
