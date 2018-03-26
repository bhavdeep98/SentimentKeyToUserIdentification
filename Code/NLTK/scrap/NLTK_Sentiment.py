#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 20:54:45 2017

@author: hemantkoti
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
import nltk
import re
import itertools

# nltk.download()

raw_text = "Paragraphs are the building blocks of papers. Many students define paragraphs in terms of length: a paragraph is a group of at least five sentences, a paragraph is half a page long, etc. In reality, though, the unity and coherence of ideas among sentences is what constitutes a paragraph. "

#input('Give us some of your opinons about life universe and everything:\n')
sentence_tokenized = nltk.sent_tokenize(raw_text)
word_tokenized = [nltk.word_tokenize(sent) for sent in sentence_tokenized]
pos_tagged_sentence = [nltk.pos_tag(sent) for sent in word_tokenized]

grammar = 'NP: {<DT>?<JJ>*<NN>}'

#grammar =   """  
#            NUMBER: {<$>*<CD>+<NN>*}
#            LOCATION: {<IN><NNP>+<,|IN><NNP>+} 
#            PROPER: {<NNP|NNPS><NNP|NNPS>+}
#            HIT: {<PROPER><NN>?<VBZ|VBN>+}
#            DATE: {<IN>(<$>*<CD>+<NN>*)}
#            """

all_chunked_words = []
for sent in pos_tagged_sentence:
   chunked_words = [] 
   cp = nltk.RegexpParser(grammar)
   result = cp.parse(sent)
   for word in result:
       if type(word) != tuple:
           target = []
           for y in word:
               target.append(y[0])
           print(target)
           chunked_words.append(target)
   all_chunked_words.append(chunked_words)

def traverse(o, tree_types=(list, tuple)):
   if isinstance(o, tree_types):
       for value in o:
           for subvalue in traverse(value, tree_types):
               yield subvalue
   else:
       yield o

listQuestions = []
for sent,chunk_list in itertools.zip_longest(word_tokenized,all_chunked_words):
   question = ""
   for word in sent:
       if word in traverse(chunk_list):
           question += " ?"
       else:
           question += " " + word
   listQuestions.append(question)

#print(listQuestions)
#print(all_chunked_words)
