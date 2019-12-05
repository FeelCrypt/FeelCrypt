# -*- coding: utf-8 -*-


# -- ==user_accounts== --
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import RegexpTokenizer
import tfidf
from IPython.display import clear_output
from nltk.corpus import stopwords
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import string


tokenizer = RegexpTokenizer(r'\w+')
porter = PorterStemmer()

def remove_punctuation(text):
    no_punct = "".join([c for c in text if c not in string.punctuation])
    return no_punct

def stem_sentence(bag_of_word):
    porter = PorterStemmer()
    return [porter.stem(word) for word in bag_of_word]

def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

def computeIDF(documents):
    import math
    N = len(documents)
    
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf

def get_tfidf(textA, textB, max_words):
    #documentA = remove_punctuation('the man went out for a walk')
    #documentB = remove_punctuation('the children sat around the fire')
    
    #bagOfWordsA = tokenizer.tokenize(documentA)
    #bagOfWordsB = tokenizer.tokenize(documentB)
    
    #uniqueWords = set(bagOfWordsA).union(set(bagOfWordsB))
    
    #numOfWordsA = dict.fromkeys(uniqueWords, 0)
    #for word in bagOfWordsA:
    #    numOfWordsA[word] += 1
    
    #numOfWordsB = dict.fromkeys(uniqueWords, 0)
    #for word in bagOfWordsB:
    #    numOfWordsB[word] += 1
    
    #tfA = computeTF(numOfWordsA, bagOfWordsA)
    #tfB = computeTF(numOfWordsB, bagOfWordsB)
    
    #idf = computeIDF([numOfWordsA, numOfWordsB])
    
    #tfidfA = computeTFIDF(tfA, idf)
    #tfidfB = computeTFIDF(tfB, idf)
    #df = pd.DataFrame([tfidfA, tfidfB])
    
    vectorizer = TfidfVectorizer(max_features=max_words)
    vectors = vectorizer.fit_transform([str(textA), str(textB)])
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    
    return pd.DataFrame(denselist, columns=feature_names)


def remove_stopwords(text):
    return [w for w in tokenizer.tokenize(text) if w.lower() not in stopwords.words("english")]

def clean_df(df):
    count = 0
    clean_text = []
    for sentence in df["text"]:
        clean_text.append(remove_stopwords(sentence))
        count+=1
        clear_output()
        print(f"{count}/{len(df)}")
    df["text"] = clean_text
    df["text"] = [" ".join(stem_sentence(x)) for x in df["text"]]
    return df

    
def get_tfidf_words(df, max_words, clean = True):
    if clean:
        df = clean_df(df)
    all_positive_texts = " ".join([df["text"][i] for i in range(len(df)) if df["label"][i] == "1"])
    all_negative_texts = " ".join([df["text"][i] for i in range(len(df)) if df["label"][i] == "0"])
    
    extracted_words = []
    cpt = 0
    for i in range(len(df)):
        cpt+=1
        clear_output()
        print(f"{cpt}/{len(df)}")
        idf = []
        if len(df["text"][i]) > 3:
            if df["label"][i] == "0":
                idf = get_tfidf(textA = df["text"][i],textB =  all_positive_texts, max_words = max_words)
            else :
                idf = get_tfidf(textA =  df["text"][i],textB = all_negative_texts, max_words = max_words)
            extracted_words.append(" ".join(list(idf.keys())))
        else :
            extracted_words.append(df["text"][i])
    df["tfidf"] = extracted_words
    
    return df

# -- ==user_accounts== --