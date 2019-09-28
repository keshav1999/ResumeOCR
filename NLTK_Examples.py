# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:55:27 2019

@author: x103447

"""

#Stop words with NLTK

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

example_sent = "This is a sample sentence, showing off the stop words filtration."

stop_words = set(stopwords.words('english'))
#print(stop_words)
word_tokens = word_tokenize(example_sent)
#print(word_tokens)

filtered_sentence = []
for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)
print(filtered_sentence)        


"""
The idea of stemming is a sort of normalizing method. Many variations of words carry the same meaning, other than when tense is involved.

The reason why we stem is to shorten the lookup, and normalize sentences.

Consider:

I was taking a ride in the car.
I was riding in the car.

This sentence means the same thing. in the car is the same. I was is the same. the ing denotes a clear past-tense in both cases, so is it truly necessary to differentiate between ride and riding, in the case of just trying to figure out the meaning of what this past-tense activity was?

No, not really.

One of the most popular stemming algorithms is the Porter stemmer, which has been around since 1979.

"""

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()
example_words = ["python","pythoner","pythoning","pythoned","pythonly"]
for w in example_words:
    print(ps.stem(w))

#Now let's try stemming a typical sentence, rather than some words
new_text = "It is important to by very pythonly while you are pythoning with python. All pythoners have pythoned poorly at least once."

words = word_tokenize(new_text)

for w in words:
    print(ps.stem(w))

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

print(lemmatizer.lemmatize("cats"))
print(lemmatizer.lemmatize("cacti"))
print(lemmatizer.lemmatize("geese"))
print(lemmatizer.lemmatize("rocks"))
print(lemmatizer.lemmatize("python"))
print(lemmatizer.lemmatize("better", pos="a"))
print(lemmatizer.lemmatize("best", pos="a"))
print(lemmatizer.lemmatize("run"))
print(lemmatizer.lemmatize("run",'v'))


"""One of the more powerful aspects of the NLTK module is the Part of Speech tagging that it can do for you. 
This means labeling words in a sentence as nouns, adjectives, verbs...etc. Even more impressive, 
it also labels by tense, and more. Here's a list of the tags, what they mean, and some examples:

NN	noun, singular 'desk'
NNS	noun plural	'desks'
NNP	proper noun, singular	'Harrison'
CC	coordinating conjunction
CD	cardinal digit
EX	existential there (like: "there is" ... think of it like "there exists")
NN	noun, singular 'desk'
POS	possessive ending	parent\'s


we're going to cover a new sentence tokenizer, called the PunktSentenceTokenizer. 
This tokenizer is capable of unsupervised machine learning, so you can actually train it on any body of text that you use.
"""

import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

#Now, let's create our training and testing data:
train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")
print(train_text)

print(sample_text)
custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

tokenized = custom_sent_tokenizer.tokenize(sample_text)


#Now we can finish up this part of speech tagging script by creating a function that will run through
#and tag all of the parts of speech per sentence like so:

def process_content():
    try:
        for i in tokenized[:5]:
            #print(i)
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            print(tagged)

    except Exception as e:
        print(str(e))


process_content()    

"""
Modifiers:->
    + = match 1 or more
    ? = match 0 or 1 repetitions.
    * = match 0 or MORE repetitions	  
    . = Any character except a new line
POS:->
    <RB.?>* = "0 or more of any tense of adverb," followed by:
    <VB.?>* = "0 or more of any tense of verb," followed by:
    <NNP>+ = "One or more proper nouns," followed by
    <NN>? = "zero or one singular noun."
"""

import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

tokenized = custom_sent_tokenizer.tokenize(sample_text)

def process_content():
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            print(chunked)
#            chunked.draw()     

    except Exception as e:
        print(str(e))

process_content()


def process_content_subtree():
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            
            print(chunked)
            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
                print(subtree)

#            chunked.draw()

    except Exception as e:
        print(str(e))

process_content_subtree()