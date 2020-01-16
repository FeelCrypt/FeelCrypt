import pandas as pd
import string
import nltk
import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import regex as re
import operator
import os
import sys
import time
import json
import csv
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from pandas.io.json import json_normalize
import operator

pd.set_option('display.max_columns', None)

def get_csv_tfidf(file_name = "TFIDF.csv"):
    start_time = time.time()
    tfidf_csv = None
    dicoTfidf = {}
    dico = { "date" : [], "words" : []}
    index = 0
    dicoTfidf = {}
    id_comments = {"date" : [], "nb_comments" : []}
    date_modify_csv = []
    df_date_to_add = pd.DataFrame()
    comments = pd.DataFrame()
    
    sys.path.append("C:/Users/Admin/Projet FeelCrypt/FeelCrypt/Valentin/")
    import dataset_v
    df = dataset_v.get_labeled_dataset(all_files = True)

    try:
        tfidf_csv = pd.read_csv(file_name)
        comments = pd.read_csv("id_comments.csv", sep=",")
        date_columns_tfidf_csv = tfidf_csv["date"].values.tolist()
        date_column_reddit = df.date.unique()

        for date in date_column_reddit:
            if date not in date_columns_tfidf_csv:
                date_modify_csv.append(date)
                df_condition = (df["date"] == date)
                df_filtered = df[df_condition]
                # Ds le cas ou la date a ete traitee mais qu'elle n'a pas ete prise en compte par la tfidf (trop peu de commentaires par exemple)
                if date not in comments["date"].values.tolist():
                    id_comments["date"].append(date)
                    id_comments["nb_comments"].append(len(df_filtered))
            else:
                condition_reddit_comments = (df["date"] == date)
                nb_comments_reddit_comments = int(len(df[condition_reddit_comments]))
                condition_id_comments = (comments["date"] == date)
                nb_comments_file_saved = int(comments[condition_id_comments].nb_comments)
                
                if nb_comments_reddit_comments != nb_comments_file_saved:
                    date_modify_csv.append(date)
                    comment_index = comments.index[comments['date'] == date].tolist()
                    comments.loc[comment_index,"nb_comments"] = nb_comments_reddit_comments

        df_date_to_add = df[df.date.isin(date_modify_csv)]
        
    except:
        date_modify_csv = df.date.unique()
        df_date_to_add = df
        
        for date in df.date.unique():
            df_condition = (df["date"] == date)
            df_filtered = df[df_condition]
            id_comments["date"].append(date)
            id_comments["nb_comments"].append(len(df_filtered))
    
    df_comments = comments.append(pd.DataFrame.from_dict(id_comments))
    df_comments.to_csv('id_comments.csv', index=False)
            
    # Pour chaque date a rajouter au fichier csv
    for date in date_modify_csv:
        dicoDate = []
        scores = []
        # Si on est sur la même date que celle recupéré par la boucle for, on continue la tfidf actuelle
        while df_date_to_add["date"].iloc[index] == date and index < len(df_date_to_add)-1:
            # on rentre au moins une fois dedans
            text_date = df_date_to_add["text"].iloc[index].split(' ')
            if df_date_to_add["score"].iloc[index] > 0 and len(text_date) > 2:
                dicoDate.append(df_date_to_add["text"].iloc[index])
                scores.append(df_date_to_add["score"].iloc[index])
            index = index + 1
        if len(dicoDate) > 0:
            # On a récupéré tous les tweets de la date que l'on veut analyser avec tfidf
            # On le convertit en Series d'abord
            dicoDate = pd.Series(dicoDate)
            # len file
            len_file = len(dicoDate)
            # remove comments with low scores
            scoreSort = np.sort(scores)
            Q1 = scores[int(len_file/4)]
            # Keep all index of comments to remove because of their lower score
            scoreIndexToRemove = []
            cpt = 0
    
            for score in scores:
                if score < Q1:
                    scoreIndexToRemove.append(cpt)
                cpt += 1
    
            dicoDateNew = dicoDate.drop(scoreIndexToRemove)
            # Preprocessing des données
            dicoDateNew = preprocessing(dicoDateNew, len_file)
            # maintenant on peut appliquer tfidf
            uniqueWords = []
            for sentence in dicoDateNew:
                words = [word for word in sentence]
                for word in words:
                    if word not in uniqueWords:
                        uniqueWords.append(word)
            uniqueWords.sort()
    
            numOfWords = dict.fromkeys(uniqueWords, 0)
            for i in range(len_file):
                try :
                    for words in dicoDateNew[i]:
                        numOfWords[words] += 1
                except KeyError:
                    i += 1
    
            tf = computeTF(dicoDateNew, uniqueWords)
            idfs = dict.fromkeys(uniqueWords, 0)
            idfs = computeIDF(dicoDateNew, len_file, idfs, numOfWords)
            tfidf = computeTF_IDF(tf, idfs)

            # On recupere les mots les plus importants
            columns = tfidf.columns.values
            dicoTFIDFWords = {}
            indexes = 0
            for label in columns:
                dicoTFIDFWords[label] = sum(tfidf[columns[indexes]])
                indexes = indexes + 1
            dicoTFIDFWords = sorted(dicoTFIDFWords.items(), key=operator.itemgetter(1), reverse=True)
            dicoMostImportantWords = dicoTFIDFWords[0:50]
            dicoWordsToKeep = [l[0] for l in dicoMostImportantWords]
            try:
                dicoWordsToKeep.remove('bitcoin')
                dicoWordsToKeep.remove('btc')
            except ValueError:
                pass
            if date in date_columns_tfidf_csv:
                tfidf_csv_date_to_replace_index = tfidf_csv.index[tfidf_csv['date'] == date].tolist()
                tfidf_csv.loc[tfidf_csv_date_to_replace_index,"words"] = " ".join(dicoWordsToKeep)
            else:
                if len(dicoWordsToKeep) > 10:
                    dico["date"].append(date)
                    dico["words"].append(" ".join(dicoWordsToKeep))
    if len(dico["date"]) != 0:
        dataframe_to_add_to_csv = pd.DataFrame(dico)
        tfidf_csv_to_save = tfidf_csv.append(dataframe_to_add_to_csv)
        tfidf_csv_to_save.to_csv('TFIDF.csv',index=False)
    else:
        tfidf_csv.to_csv('TFIDF.csv',index=False)
        
def remove_punctuation(text):
    no_punct = "".join([c for c in text if c not in string.punctuation])
    return no_punct

def remove_stopwords(text):
    words = [w for w in text if w not in stopwords.words('english')]
    return words

def remove_links(text):
    words = [w for w in text if not len(w) > 20]
    return words

def stem_sentence(sentence):
    porter = PorterStemmer()
    for i in range(len(sentence)):
        word = porter.stem(sentence[i])
        sentence[i] = word
    return sentence

# Remove all "/u/", "/r", "/r", "\n" and numbers
def preprocessing(commentArray, len_file):
    for i in range(len_file):
        try:
            commentArray[i] = re.sub(r"(\/\w\/|\w\/)", "", commentArray[i])
            commentArray[i] = re.sub(r"\\n?t?", "", commentArray[i])
            commentArray[i] = re.sub(r"[0-9]*", "", commentArray[i])
        except KeyError:
            continue
    
    # punctuation
    commentArray = commentArray.apply(lambda x: remove_punctuation(x))
    tokenizer = RegexpTokenizer(r'\w+')
    commentArray = commentArray.apply(lambda x : tokenizer.tokenize(x.lower()))
    
    # remove small words
    for i in range(len_file):
        try:
            for word in commentArray[i]:
                if len(word) < 3:
                    commentArray[i].remove(word)
        except KeyError:
            continue
    # remove stopwords
    commentArray = commentArray.apply(lambda x : remove_stopwords(x))

    # reddit link
    commentArray = commentArray.apply(lambda x : remove_links(x))
    
    return commentArray

def computeTF(file, uniqueWords):
    tf = []
    index = 0
    
    try :
        for sentence in file:
            tf.append(dict.fromkeys(uniqueWords, 0))
            for word in sentence:
                tf[index][word] += 1 / len(sentence)
            index += 1
    except KeyError :
        print("error")
    return tf

def computeIDF(file, len_file, idfs, numOfWords):
    # Pour chaque doc, pour chaque mot on regarde sa tf
    for x, y in idfs.items():
        count = 0
        for i in range(len_file):
            try:
                for word in file[i]:
                    if x == word:
                        count += 1
                        break
            except KeyError:
                i += 1
        if count != 0:
            idfs[x] = math.log(numOfWords[x] / count)
    return idfs

def computeTF_IDF(tf, idfs):
    tab = []
    for i in range(len(tf)):
        dico = {}
        for mot in tf[i]:
            dico[mot] = tf[i][mot] * idfs[mot]
        tab.append(dico)
    tfidf = pd.DataFrame(tab)
    return tfidf