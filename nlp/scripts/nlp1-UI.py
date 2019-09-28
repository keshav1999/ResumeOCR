# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:09:13 2019

@author: X103447
"""

import sys
import re
from pathlib import Path

filename = str(sys.argv)
file = Path(sys.argv[1])
fileExt = sys.argv[2]

#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))

#fileExt = Path(sys.argv[2])
#print(fileExt)
#file=r"C:\Users\x103447\Desktop\Testing\SSIS\Python\Learn PY\NLP\Resume\neeraj goel.docx" 
#fileExt = "docx"
#print(file)
    
#file = r"C:\Users\x122866\Desktop\atul sharma.pdf"
    
#############################################################
#------convertPDFToText--------------------------------------
#############################################################
import io
import nltk

if fileExt == "pdf":
#    print("Enter pdf")
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    
    def convertPDFToText(path):
        #to store the shared resources like font or images
        rsrcmgr = PDFResourceManager()
        #to read string either of 8 bit or unicode
        retstr = io.StringIO()
        #UTF stands for Unicode Transformation Format. The '8' means it uses 8-bit blocks to represent a character
        codec = 'utf-8'
        # to perform layout analysis like LTTextBox LTTextLine
        laparams = LAParams()
        #to transalte it to whatever you need
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        #to Open the file in read binary mode
        fp = io.FileIO(path, 'rb')
        #to process the page content 
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set() 
        
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
        fp.close()
        device.close()
        string = retstr.getvalue()
        retstr.close()
        return string
    
    inputString = convertPDFToText(file)
elif fileExt == "docx":
#    print("Enter word")
    from docx import Document

    def convertDocxToText(path):
    	document = Document(path)
    	return "\n".join([para.text for para in document.paragraphs])
    
    inputString = convertDocxToText(file)
else:
    print("Error")
    
#abc = convertPDFToText(r"C:\Users\x103447\Desktop\Testing\SSIS\Python\Learn PY\NLP\Resume\atul sharma.pdf")
#print(abc)
#file = r"C:\Users\x103447\Desktop\Testing\SSIS\Python\Learn PY\NLP\Resume\atul sharma.pdf"

##inputString = convertPDFToText(file)

#file
#inputString = abc

def getEmail(inputString, infoDict): 
    email = None
    try:
        pattern = re.compile(r'\S*@\S*')
        matches = pattern.findall(inputString) # Gets all email addresses as a list
        email = matches
    except Exception as e:
        print (e)
    infoDict['email'] = email
#    print(email)
    return email

info = {}
info['email'] = getEmail(inputString,info)

#print(info['email'])

#############################################################
#get phone number  
#############################################################
def getPhone(inputString, infoDict, debug=False):
    number = None
    try:
        pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
            # Understanding the above regex
            # +91 or (91) -> [+(]? \d+ -?
            # Metacharacters have to be escaped with \ outside of character classes; inside only hyphen has to be escaped
            # hyphen has to be escaped inside the character class if you're not incidication a range
            # General number formats are 123 456 7890 or 12345 67890 or 1234567890 or 123-456-7890, hence 3 or more digits
            # Amendment to above - some also have (0000) 00 00 00 kind of format
            # \s* is any whitespace character - careful, use [ \t\r\f\v]* instead since newlines are trouble
        match = pattern.findall(inputString)
        # match = [re.sub(r'\s', '', el) for el in match]
            # Get rid of random whitespaces - helps with getting rid of 6 digits or fewer (e.g. pin codes) strings
        # substitute the characters we don't want just for the purpose of checking
        match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el))>6]
            # Taking care of years, eg. 2001-2004 etc.
        match = [re.sub(r'\D$', '', el).strip() for el in match]
            # $ matches end of string. This takes care of random trailing non-digit characters. \D is non-digit characters
        match = [el for el in match if len(re.sub(r'\D','',el)) <= 15]
            # Remove number strings that are greater than 15 digits
        try:
            for el in list(match):
                # Create a copy of the list since you're iterating over it
                if len(el.split('-')) > 3: continue # Year format YYYY-MM-DD
                for x in el.split("-"):
                    try:
                        # Error catching is necessary because of possibility of stray non-number characters
                        # if int(re.sub(r'\D', '', x.strip())) in range(1900, 2100):
                        if x.strip()[-4:].isdigit():
                            if int(x.strip()[-4:]) in range(1900, 2100):
                                # Don't combine the two if statements to avoid a type conversion error
                                match.remove(el)
                    except:
                        pass
        except:
            pass
        number = match
    except:
        pass
    
    infoDict['phone'] = number
    return number

info['phone'] = getPhone(inputString,info)

#print(info['phone'])
#############################################################
#Get Name
#############################################################
def getName(inputString, infoDict, debug=False):    
    lines = [el.strip() for el in inputString.split("\n") if len(el) > 0]
    lines = [nltk.word_tokenize(el) for el in lines]
    lines = [nltk.pos_tag(el) for el in lines]
    #print(lines)
    grammar = r'NAME: {<NN.*>*}'
    #grammar = r'NAME: {<NN.*><NN.*><NN.*>*}'
    chunkParser = nltk.RegexpParser(grammar)
    # Reads Indian Names from the file, reduce all to lower case for easy comparision [Name lists]
    indianNames = open(r"C:\XL_Apps\Xampp\htdocs\nlp\scripts\allNames.txt", "r").read().lower()
    # Lookup in a set is much faster
    indianNames = set(indianNames.split())
    nameHits = []
    otherNameHits = []
    name = None
    for tagged_tokens in lines:
        chunked_tokens = chunkParser.parse(tagged_tokens)
        for subtree in chunked_tokens.subtrees():
            if subtree.label() == 'NAME':
                for ind, leaf in enumerate(subtree.leaves()):
                    if leaf[0].lower() in indianNames and 'NN' in leaf[1]:
    #                    print(leaf)
    #                    for el in subtree.leaves()[ind:ind+3]:
    #                        print(el[0])
    #                        hit = " ".join(el[0])
                        hit = " ".join([el[0] for el in subtree.leaves()[ind:ind+3]])
                        nameHits.append(hit)
#                        print(nameHits) 
    
    # Going for the first name hit
    if len(nameHits) > 0:
    #    print(nameHits[0])
#        nameHits = [re.sub(r'[^a-zA-Z \-]', '', el).strip() for el in nameHits] 
        name = " ".join([el[0].upper()+el[1:].lower() for el in nameHits[0].split() if len(el)>0])
#        otherNameHits = nameHits[1:]
    
#    print(nameHits)    
#    print(otherNameHits)    
#    print(name) #Final Name result
    infoDict['name'] = name
    return name

info['name'] = getName(inputString,info)

print(info['name'])
print(info['phone'])
print(info['email'])

##################Added by Anand

#############################################################
# get Experience details
#############################################################
sen = ""
experience = []
lines = [el.strip() for el in inputString.split("\n") if len(el) > 0]
lines = [nltk.word_tokenize(el) for el in lines]
lines = [nltk.pos_tag(el) for el in lines]
try:
    for sentence in lines:#find the index of the sentence where the degree is find and then analyse that sentence
            sen=" ".join([words[0].lower() for words in sentence]) #string of words in sentence
            if re.search('experience',sen):
                sen_tokenised= nltk.word_tokenize(sen)
                tagged = nltk.pos_tag(sen_tokenised)
                entities = nltk.chunk.ne_chunk(tagged)
                for subtree in entities.subtrees():
                    for leaf in subtree.leaves():
                        if leaf[1]=='CD':
#                            experience=leaf[0]
                            experience.append(leaf[0])
except Exception as e:
#    print (traceback.format_exc())
    print (e)

#print(experience)
if experience == []:
    print("NA")
else:
    print(max(experience)) #if list has multiple experience

#if list has multiple experience

#old running code
#sen = ""
#experience = []
#lines = [el.strip() for el in inputString.split("\n") if len(el) > 0]
#lines = [nltk.word_tokenize(el) for el in lines]
#lines = [nltk.pos_tag(el) for el in lines]
#try:
#    for sentence in lines:#find the index of the sentence where the degree is find and then analyse that sentence
#            sen=" ".join([words[0].lower() for words in sentence]) #string of words in sentence
#            if re.search('experience',sen):
#                sen_tokenised= nltk.word_tokenize(sen)
#                tagged = nltk.pos_tag(sen_tokenised)
#                entities = nltk.chunk.ne_chunk(tagged)
#                for subtree in entities.subtrees():
#                    for leaf in subtree.leaves():
#                        if leaf[1]=='CD':
##                            experience=leaf[0]
#                            experience.append(leaf[0])
#except Exception as e:
##    print (traceback.format_exc())
#    print (e)
#
##print(experience)
#if experience == []:
#    print("NA")
#else:
#    print(experience) #if list has multiple experience

####################Qualification$##########   
import nltk, os, subprocess, code, glob, re, traceback, sys, inspect
from time import clock, sleep
from pprint import pprint
import json
import zipfile 

#self.Qualification(inputString,info)

def getQualification(inputString,infoDict,D1,D2):
    #key=list(qualification.keys())
    qualification={'institute':'','year':''}
    nameofinstitutes=open(r'C:\XL_Apps\Xampp\htdocs\nlp\scripts\nameofinstitutes.txt','r').read().lower()#open file which contains keywords like institutes,university usually  fond in institute names
    nameofinstitues=set(nameofinstitutes.split())
    instiregex=r'INSTI: {<DT.>?<NNP.*>+<IN.*>?<NNP.*>?}'
    chunkParser = nltk.RegexpParser(instiregex)

    try:           
        index=[]
        line=[]#saves all the lines where it finds the word of that education
        for ind, sentence in enumerate(lines):#find the index of the sentence where the degree is find and then analyse that sentence
            sen=" ".join([words[0].lower() for words in sentence]) #string of words
            if re.search(D1,sen) or re.search(D2,sen):
                index.append(ind)  #list of all indexes where word Ca lies
        if index:#only finds for Ca rank and CA year if it finds the word Ca in the document
            
            for indextocheck in index:#checks all nearby lines where it founds the degree word.ex-'CA'
                for i in [indextocheck,indextocheck+1]: #checks the line with the keyword and just the next line to it
                    try:
                        try:
                            wordstr=" ".join(words[0] for words in lines[i])#string of that particular line
                        except:
                            wordstr=""
                        #if re.search(r'\D\d{1,3}\D',wordstr.lower()) and qualification['rank']=='':
                                #qualification['rank']=re.findall(r'\D\d{1,3}\D',wordstr.lower())
                                #line.append(wordstr)
                        if re.search(r'\b[21][09][8901][0-9]',wordstr.lower()) and qualification['year']=='':
                                qualification['year']=re.findall(r'\b[21][09][8901][0-9]',wordstr.lower())
                                line.append(wordstr)
                        chunked_line = chunkParser.parse(lines[i])#regex chunk for searching univ name
                        for subtree in chunked_line.subtrees():
                                if subtree.label()=='INSTI':
                                    for ind,leaves in enumerate(subtree):
                                        if leaves[0].lower() in nameofinstitutes and leaves[1]=='NNP' and qualification['institute']=='':
                                            qualification['institute']=' '.join([words[0]for words in subtree.leaves()])
                                            line.append(wordstr)
                            
                    except Exception as e:
                        print (traceback.format_exc())

        if D1=='':
            infoDict['%sinstitute'%D1] =" "
        else:
            if qualification['institute']:
                infoDict['%sinstitute'%D1] = str(qualification['institute'])
            else:
                infoDict['%sinstitute'%D1] = "NULL"
        if qualification['year']:
            infoDict['%syear'%D1] = int(qualification['year'][0])
        else:
            infoDict['%syear'%D1] =0
        infoDict['%sline'%D1]=list(set(line))
    except Exception as e:
        print (traceback.format_exc())
        print (e) 

###Sfift+tab to move left

info = {}
info['extension'] = inputString
info['fileName'] = 'resume'

debug=False 
degre=[]
getQualification(inputString,info,'c\.?a\W+','chartered accountant')
if info['%sline'%'c\.?a\W+']:
    degre.append('Chartered Accountant')
getQualification(inputString,info,'icwa\W+','institute of cost and works accountants')
if info['%sline'%'icwa\W+']:
    degre.append('Institute of Cost And Works Accountants')
getQualification(inputString,info,'b\.?\s*com\W+','bachelor of commerce')
if info['%sline'%'b\.?\s*com\W+']:
    degre.append('Bachelor of Commerce')
getQualification(inputString,info,'m\.?com\W+','masters of commerce')
if info['%sline'%'m\.?com\W+']:
    degre.append('Masters of Commerce') 
getQualification(inputString,info,'b\.?tech\W+','bachelor of technology')
if info['%sline'%'b\.?tech\W+']:
    degre.append('Bachelor Of Technology')
getQualification(inputString,info,'mba\W+','master of business administration')
if info['%sline'%'mba\W+']:
    degre.append('Master of Business Administration')
if degre:
    info['degree'] = degre
else:
    info['degree'] = "NONE"   
if debug:
    print ("\n", pprint(info), "\n")   
    code.interact(local=locals())

import re

pattern=re.compile(r'^.*line.*')
str1=""
str2=""
for key,value in info.items(): 
    if pattern.match(key):
        if value not in ('NULL','',0,[]):
            str1=str(value)
            str2=str2+">> "+str1[2:-2]+"."
            
print(degre)          
print (str2)


#inputStr = ''
#info = {}
#
#info['extension'] = inputString
#
#def getQualification(inputString,infoDict,D1,D2):
#    #key=list(qualification.keys())
#    qualification={'institute':'','year':''}
#    nameofinstitutes=open(r'C:\xampp\htdocs\nlp\scripts\nameofinstitutes.txt','r').read().lower()#open file which contains keywords like institutes,university usually  fond in institute names
#    nameofinstitues=set(nameofinstitutes.split())
#    instiregex=r'INSTI: {<DT.>?<NNP.*>+<IN.*>?<NNP.*>?}'
#    chunkParser = nltk.RegexpParser(instiregex)    
#    
#    try:           
#        index=[]
#        line=[]#saves all the lines where it finds the word of that education
#        for ind, sentence in enumerate(lines):#find the index of the sentence where the degree is find and then analyse that sentence
#            sen=" ".join([words[0].lower() for words in sentence]) #string of words
#            if re.search(D1,sen) or re.search(D2,sen):
#                index.append(ind)  #list of all indexes where word Ca lies
#        if index:#only finds for Ca rank and CA year if it finds the word Ca in the document
#            
#            for indextocheck in index:#checks all nearby lines where it founds the degree word.ex-'CA'
#                for i in [indextocheck,indextocheck+1]: #checks the line with the keyword and just the next line to it
#                    try:
#                        try:
#                            wordstr=" ".join(words[0] for words in lines[i])#string of that particular line
#                        except:
#                            wordstr=""
#                        #if re.search(r'\D\d{1,3}\D',wordstr.lower()) and qualification['rank']=='':
#                                #qualification['rank']=re.findall(r'\D\d{1,3}\D',wordstr.lower())
#                                #line.append(wordstr)
#                        if re.search(r'\b[21][09][8901][0-9]',wordstr.lower()) and qualification['year']=='':
#                                qualification['year']=re.findall(r'\b[21][09][8901][0-9]',wordstr.lower())
#                                line.append(wordstr)
#                        chunked_line = chunkParser.parse(lines[i])#regex chunk for searching univ name
#                        for subtree in chunked_line.subtrees():
#                                if subtree.label()=='INSTI':
#                                    for ind,leaves in enumerate(subtree):
#                                        if leaves[0].lower() in nameofinstitutes and leaves[1]=='NNP' and qualification['institute']=='':
#                                            qualification['institute']=' '.join([words[0]for words in subtree.leaves()])
#                                            line.append(wordstr)
#                            
#                    except Exception as e:
#                        print (traceback.format_exc())
#
#        if D1=='':
#            infoDict['%sinstitute'%D1] =" "
#        else:
#            if qualification['institute']:
#                infoDict['%sinstitute'%D1] = str(qualification['institute'])
#            else:
#                infoDict['%sinstitute'%D1] = "NULL"
#        if qualification['year']:
#            infoDict['%syear'%D1] = int(qualification['year'][0])
#        else:
#            infoDict['%syear'%D1] =0
#        infoDict['%sline'%D1]=list(set(line))
#    except Exception as e:
#        print (traceback.format_exc())
#        print (e) 
#
####Sfift+tab to move left
#
#info = {}
#info['extension'] = inputString
#info['fileName'] = 'resume'
#
#debug=False 
#degre=[]
#getQualification(inputString,info,'c\.?a\W+','chartered accountant')
#if info['%sline'%'c\.?a\W+']:
# degre.append('ca')
#getQualification(inputString,info,'icwa','icwa')
#if info['%sline'%'icwa']:
# degre.append('icwa')
#getQualification(inputString,info,'b\.?com','bachelor of commerce')
#if info['%sline'%'b\.?com']:
# degre.append('b.com')
#getQualification(inputString,info,'m\.?com','masters of commerce')
#if info['%sline'%'m\.?com']:
# degre.append('m.com') 
#getQualification(inputString,info,'b\.?tech','bachelor of technology')
#if info['%sline'%'b\.?tech']:
# degre.append('b.tech')
#getQualification(inputString,info,'mba','mba')
#if info['%sline'%'mba']:
# degre.append('mba')
#if degre:
#    info['degree'] = degre
#else:
#    info['degree'] = "NONE"   
#if debug:
#    print ("\n", pprint(info), "\n")   
#    code.interact(local=locals())
#print(degre)


#==============================================================================
# for key,value in info.items():
#     if key not in ('extension','fileName'):
#         if value in ('NULL','',0,[]):
#           print (key, ": NA" )  
#         else: 
#           print (key, ":" , value )
#==============================================================================
#for key,value in info.items():
##==============================================================================
##   if key in ('c\.?a\W+institute', 'icwainstitute', 'b\.?cominstitute', 'm\.?cominstitute', 
##      'b\.?techinstitute', 'mbainstitute') and value not in ('NULL','',0,[]):
##      print (value)
##      
##   if key in ('c\.?a\W+year', 'icwayear', 'b\.?comyear', 'm\.?comyear', 
##      'b\.?techyear', 'mbayear') and value not in (0,[]):
##      print ("Year : ", value)
##==============================================================================     
#  if key in ('c\.?a\W+line', 'icwaline', 'b\.?comline', 'm\.?comline', 
#     'b\.?techline', 'mbaline') and value not in (0,[]):
#     print (value)


