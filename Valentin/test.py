# -*- coding: utf-8 -*-


# -- ==user_accounts== --
from numpy import array
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
import math
def test(a):
    print("hello", a)

# -- ==user_accounts== --