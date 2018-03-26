# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 14:11:29 2017

@author: HemantKo
"""
import NLTK_StanfordNER_Register as register
mean = ""

def start(answer, random_question_token, username):
    
    answer_sentiment = register.GetListOfSentimentsforeachSentence(answer)
    
    with open('output\\'+ username +'.txt', 'r') as myfile:
        all_tokens_sentiment_string=myfile.read().replace('\n', '')
        
    all_tokens_sentiment = eval(all_tokens_sentiment_string)
    
    def EvaluateSentiment(all_tokens_sentiment, answer_sentiment, random_question_token):
        global mean
        mean = register.MeanFromList(answer_sentiment)
        return (all_tokens_sentiment[random_question_token] - 0.5 <= mean and mean <= all_tokens_sentiment[random_question_token] + 0.5)
        
    if(EvaluateSentiment(all_tokens_sentiment, answer_sentiment, random_question_token)):
        return "Sentiment Matched! Login Successful. Username = " + username + ", sentiment = " + str(all_tokens_sentiment[random_question_token]) + ", Token = " + random_question_token + ", Current_Sentence_Mean = " + str(mean)
    else:
        return "Sentiment Not Matched! Login Unsuccessful. Username = " + username + ", sentiment = " + str(all_tokens_sentiment[random_question_token]) + ", Token = " + random_question_token + ", Current_Sentence_Mean = " + str(mean)