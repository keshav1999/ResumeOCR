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


# Finding text based on following types:
# 1. FindAbs - Just use regex to filter
# 2. FindList - Use the regex and grammar to search if regex specified and
#               Use the mentioned file to pick the specified names
# 3. NLTK - Use the regex and grammar to search
# 4. None of the above - Search for the keyword and use text after it using Regex


# Find mentioned fields values using mapping
def find_Abs(textstr, field_match):

    Pattern = re.compile(field_match[2])
    matches = Pattern.findall(textstr)
    
    ind = 0
    col_names=['Field','Match_Field','text']
    MatchedValues = pd.DataFrame(index=range(1,1000), columns=col_names)

    
    for i in matches:
        MatchedValues.iloc[ind,0]= field_match[0]
        MatchedValues.iloc[ind,1]= field_match[1]
        MatchedValues.iloc[ind,2] = i

    print(MatchedValues)