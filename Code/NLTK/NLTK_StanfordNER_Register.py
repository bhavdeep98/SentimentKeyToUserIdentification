"""
Created on Mon Dec 4 09:00:17 2017
@author: HemantKo
"""
import nltk
from nltk.tag import StanfordNERTagger
from pycorenlp import StanfordCoreNLP
import itertools
import json

# To download NLTK packages
# nltk.download()

# Returns the Mean from a list of numbers
def MeanFromList(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def WriteChunkedWordsToFile(classified_text):
    chunked_words = []  
    for word in classified_text:
        if(word[1] != 'O'):
            chunked_words.append(word[0])
    return chunked_words       

# Traverses through a list of lists
def traverse(o, tree_types=(list, tuple)):
   if isinstance(o, tree_types):
       for value in o:
           for subvalue in traverse(value, tree_types):
               yield subvalue
   else:
       yield o
       
# Returns a Dictionary of key-value pair, where key is the token and value is the average sentiment
def GetListOfSentimentsforeachToken(all_chunked_words,sentiment_list):
    all_tokens_sentiment = {}
    for chunk_list,sentiment in itertools.zip_longest(all_chunked_words,sentiment_list): 
        for word in chunk_list:
            if word in all_tokens_sentiment:
                all_tokens_sentiment[word].append(sentiment)
            else:
                all_tokens_sentiment[word] = []
                all_tokens_sentiment[word].append(sentiment)
    
    for key in all_tokens_sentiment:
        all_tokens_sentiment[key] = MeanFromList(all_tokens_sentiment[key])
    return all_tokens_sentiment

# Stanford Core NLP library which returns the Sentiment value list for every Sentence
def GetListOfSentimentsforeachSentence(raw_text):
    # Initiate StandfordCore NLP object
    nlp = StanfordCoreNLP('http://localhost:9000')
    
    result = nlp.annotate(raw_text,
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 100000,
                   })
    
    sentiment_list = []
    for sent_itr in result["sentences"]:
        sentiment_list.append(int(sent_itr["sentimentValue"]))
        
    return sentiment_list

# Returns a chunk of all the Named Entities as a list
# Combines similar entities together
def GetChunkWords(classified_text):
    chunked_words = []  
    current = ""
    previous = ""
    groupsimilarstring = ""
    for word in classified_text:
        current = word[1]
        if(current == 'PERSON' or current == 'LOCATION' or current == 'ORGANIZATION'):
            if(current == previous):
                groupsimilarstring += " "+ word[0]
            else:
                if(groupsimilarstring != "" and groupsimilarstring not in chunked_words):
                    chunked_words.append(groupsimilarstring)
                groupsimilarstring = word[0]
        elif(current != 'O'):
            if(word[0] != "" and word[0] not in chunked_words):
                chunked_words.append(word[0])
        else:
            if(groupsimilarstring != "" and groupsimilarstring not in chunked_words):
                chunked_words.append(groupsimilarstring)
            groupsimilarstring = ""
        previous = current
    return chunked_words

def start(raw_text, username):
    # Standford Classifier and Standord NER Path
    stanford_classifier = '..\stanford-ner-2017-06-09\classifiers\english.muc.7class.distsim.crf.ser.gz'
    stanford_ner_path = '..\stanford-ner-2017-06-09\stanford-ner.jar'

    # Creating Tagger Object
    st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')

#    # Get the Input
#    with open('input.txt', 'r') as myfile:
#        raw_text=myfile.read().replace('\n', '')

    # Tokenize the Sentence and the Words
    sentence_tokenized = nltk.sent_tokenize(raw_text)
    word_tokenized = [nltk.word_tokenize(sent) for sent in sentence_tokenized]

    # Creates a list of lists that stores all the chunked words (with entities) for each and every tokenized sentence
    all_chunked_words = []
    for words in word_tokenized:
        chunked_words = GetChunkWords(st.tag(words))
        all_chunked_words.append(chunked_words)

    namedentities = []
    for words in word_tokenized:
        namedentities.append(WriteChunkedWordsToFile(st.tag(words)))
    
    with open('output\\namedentities.txt', 'w') as outfile:
        json.dump(namedentities, outfile) 
    
    # Creates a list of sentiment values for each sentence in the raw text
    # result = GetListOfSentimentsforeachSentence(raw_text)
    sentiment_list = GetListOfSentimentsforeachSentence(raw_text)
    
    # Creates a Dictionary of key-value pair, where key is the token and value is the average sentiment
    all_tokens_sentiment = GetListOfSentimentsforeachToken(all_chunked_words,sentiment_list)

    # Register Code     
    with open('output\\'+ username +'.txt', 'w+') as outfile:
        json.dump(all_tokens_sentiment, outfile)
