# import libs
from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd

# data processing libs
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# data preprocessing
def remove_newline(text):
    return ''.join(text.splitlines())

def replace_contractions(text):
    text = re.sub(r"won't", "will not", str(text))
    text = re.sub(r"would't", "would not",str(text))
    text = re.sub(r"could't", "could not",str(text))
    text = re.sub(r"\'d",  " would",str(text))
    text = re.sub(r"can't", "can not",str(text))
    text = re.sub(r"n\'t", " not", str(text))
    text = re.sub(r"\'re", " are", str(text))
    text = re.sub(r"\'s", " is", str(text))
    text = re.sub(r"\'ll", " will", str(text))
    text = re.sub(r"\'t", " not", str(text))
    text = re.sub(r"\'count=ve", " have", str(text))
    text = re.sub(r"\'m", " am", str(text))
    return str(text)

def remove_punc(text):
    for punc in string.punctuation:
        text = text.replace(punc, '')
    return text

def remove_non_char(text):
    text = re.sub('[0-9]+', '', str(text))
    return text

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

def text_data_preprossing(text):
    
    # remove new line
    text = text.apply(remove_newline)

    # replace contraction
    text = text.apply(replace_contractions)

    # remove punctuation
    text = text.apply(remove_punc)

    # remove extra space 
    text = text.apply(lambda x: re.sub(' +', ' ', str(x)))

    # remove stop words
    stop = stopwords.words("english")
    text = text.apply(lambda x: " ".join([x for x in x.split() if x not in stop]))

    # remove all non_char
    text = text.apply(remove_non_char)

    #covert to lowercase
    text = text.str.lower()

    # lemmatization
    text = text.apply(lemmatize_text)

    return text

# MODEL DEPLOYMENT----------------------------------------------------------------------
app = Flask(__name__)


# load sentiment analysis model
model = pickle.load(open(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\sentiment_analysis_model.pkl", 'rb'))

# load template


# load 
@app.route("/")
def index():
    return render_template('index.html')
    

@app.route('/run_pre', methods=['POST'])
def predict():

    if request.method == 'POST':
        text = request.form['text']

        # text data processing
        df = pd.DataFrame([text], columns=['text'])

            # data preprocessing
        def remove_newline(text):
            return ''.join(text.splitlines())

        def replace_contractions(text):
            text = re.sub(r"won't", "will not", str(text))
            text = re.sub(r"would't", "would not",str(text))
            text = re.sub(r"could't", "could not",str(text))
            text = re.sub(r"\'d",  " would",str(text))
            text = re.sub(r"can't", "can not",str(text))
            text = re.sub(r"n\'t", " not", str(text))
            text = re.sub(r"\'re", " are", str(text))
            text = re.sub(r"\'s", " is", str(text))
            text = re.sub(r"\'ll", " will", str(text))
            text = re.sub(r"\'t", " not", str(text))
            text = re.sub(r"\'count=ve", " have", str(text))
            text = re.sub(r"\'m", " am", str(text))
            return str(text)

        def remove_punc(text):
            for punc in string.punctuation:
                text = text.replace(punc, '')
            return text

        def remove_non_char(text):
            text = re.sub('[0-9]+', '', str(text))
            return text

        def lemmatize_text(text):
            lemmatizer = WordNetLemmatizer()
            words = text.split()
            words = [lemmatizer.lemmatize(word) for word in words]
            return ' '.join(words)

        def text_data_preprossing(text):
            
            # remove new line
            text = text.apply(remove_newline)

            # replace contraction
            text = text.apply(replace_contractions)

            # remove punctuation
            text = text.apply(remove_punc)

            # remove extra space 
            text = text.apply(lambda x: re.sub(' +', ' ', str(x)))

            # remove stop words
            stop = stopwords.words("english")
            text = text.apply(lambda x: " ".join([x for x in x.split() if x not in stop]))

            # remove all non_char
            text = text.apply(remove_non_char)

            #covert to lowercase
            text = text.str.lower()

            # lemmatization
            text = text.apply(lemmatize_text)

            return text

        df['text'] = text_data_preprossing(df['text'])
        
        # load model

        model_pp = pickle.load(open(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\pipeline.pkl", 'rb'))

        pred = model_pp.predict(df['text'])

        if pred == 1:
            prediction = 'Positive'

        elif pred == 0:
            prediction = 'Negative'
        

        #result
        return render_template('index.html', result = "This is predicted as {} review".format(prediction), original_input = "Original input: {} ".format(text))
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)