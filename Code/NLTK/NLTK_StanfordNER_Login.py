# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 12:01:06 2017

@author: HemantKo
"""
import NLTK_StanfordNER_Register as register
import random

def start(username):
    with open('output\\'+ username +'.txt', 'r') as myfile:
        all_chunked_words_string=myfile.read().replace('\n', '')
        
    all_chunked_words = eval(all_chunked_words_string)
    
    # Creates a Question based on the entities found
    listQuestions = []
    for word in all_chunked_words:
        question = "What is your opinion on '" + word + "'?"
        if(question not in listQuestions):
            listQuestions.append(question)
    
#    with open('output\\question.txt', 'w+') as outfile:
#        outfile.write(random.choice(listQuestions)) 

    random_question =  random.choice(listQuestions)
    random_question_token = random_question.split("'")[1]
    return random_question, random_question_token

#    random_question_token = random_question.split("'")[1]
#    answer_sentiment = register.GetListOfSentimentsforeachSentence(answer)
#    
#    def EvaluateSentiment(all_tokens_sentiment, answer_sentiment, random_question_token):
#        return all_tokens_sentiment[random_question_token] - 1 <= register.MeanFromList(answer_sentiment) and register.MeanFromList(answer_sentiment) <= all_tokens_sentiment[random_question_token] + 1
#        
#    if(EvaluateSentiment(all_tokens_sentiment, answer_sentiment, random_question_token)):
#        print("Sentiment Matched!")
#    else:
#        print("Sentiment Not Matched!")