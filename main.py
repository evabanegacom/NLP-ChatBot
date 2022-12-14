import os
import warnings
import nltk
import string
import random 
#from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText

#from openfabric_pysdk.context import OpenfabricExecutionRay
#from openfabric_pysdk.loader import ConfigClass
from time import time

# nltk.download('omw-1.4')

f=open("chatbot.txt", "r", errors='ignore')
raw=f.read()
raw=raw.lower()
nltk.download('punkt')
nltk.download('wordnet')
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

Greetings_Input = ("hello", "hi", "greetings", "sup", "what's up","hey",)
Greetings_Response = ["hi", "hey", "nods", "hi there", "hello", "I am glad! You are talking to me"]

def config(sentence):
    for word in sentence.split():
        if word.lower() in Greetings_Input:
            return random.choice(Greetings_Response)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def execute(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

flag=True
print("ROBO: My name is Robot. I will answer your queries about Science. If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("ROBOT: You are welcome..")
        else:
            if(config(user_response)!=None):
                print("ROBOT: "+config(user_response))
            else:
                print("ROBOT: ",end="")
                print(execute(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("ROBOT: Bye! take care..")