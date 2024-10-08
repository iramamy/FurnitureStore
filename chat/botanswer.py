import nltk
import json
import random
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import os

# nltk.download('punkt')
# nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

script_dir = os.path.dirname(os.path.abspath(__file__))

intents_file = os.path.join(script_dir, 'data', 'intents.pkl')
words_file = os.path.join(script_dir, 'data', 'words.pkl')
classes_file = os.path.join(script_dir, 'data', 'classes.pkl')
model_file = os.path.join(script_dir, 'data', 'chatbot_model.h5')

model = load_model(model_file)

with open(intents_file, 'rb') as file:
    intents = pickle.load(file)

with open(words_file, 'rb') as file:
    words = pickle.load(file)

with open(classes_file, 'rb') as file:
    classes = pickle.load(file)

def clean_up_sentence(sentence):

    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

    return sentence_words


def bow(sentence, words, show_details=False):

    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))


def predict_class(sentence, model):

    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []

    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})

    return return_list


def getResponse(ints, intents_json):

    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']

    result = "I'm sorry, I don't understand your request."

    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break

    return result


def chatbot_response(text):
    
    ints = predict_class(text, model)
    res = getResponse(ints, intents)

    return res
