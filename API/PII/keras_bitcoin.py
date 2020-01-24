# -*- coding: utf-8 -*-


# -- ==user_accounts== --
from numpy import array
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Flatten
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.layers.embeddings import Embedding
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
import math

available_activation_functions = ["tanh", "elu", "softmax", "selu", "softplus", "softsign", "relu", "sigmoid", "hard_sigmoid", "exponential", "linear"]

def get_unique_words_count(texts):
    
    words_set = set()
    for sentence in texts:
        tokenize_word = word_tokenize(sentence)
        for word in tokenize_word:
            words_set.add(word)
    return len(words_set)

def get_above_multiple(num, divisor):
    return math.ceil(num / divisor) * divisor

def encode_data(texts):
    texts = [str(text) for text in texts]
    vocab_length = get_above_multiple(get_unique_words_count(texts), 10)
    coded_sentences = [one_hot(sentence, vocab_length) for sentence in texts]
    max_sentence_size = max(list(map(lambda sentence : len(word_tokenize(sentence)), texts)))
    padded_coded_sentences = pad_sequences(coded_sentences, max_sentence_size, padding='post')
    return padded_coded_sentences, vocab_length, max_sentence_size

def get_train_test_data(texts, labels):
    padded_coded_sentences, vocab_length, max_sentence_size = encode_data(texts)
    texts_train, texts_test , labels_train, labels_test = train_test_split(padded_coded_sentences, labels , test_size = 0.20)
    return texts_train, texts_test, labels_train, labels_test, vocab_length,max_sentence_size

#model.add(Conv1D(250,3,padding='valid',activation='sigmoid',strides=(2,2)))
#model.add(Dense(250, activation="softplus"))
#model.add(Dense(1, activation="sigmoid"))
def get_model(texts_train, labels_train, vocab_length, max_sentence_size, epochs = 100, batch_size=100, activations_functions = ["sigmoid"], verbose = 0, dropouts = []):
    model = Sequential()
    model.add(Embedding(vocab_length, 20, input_length=max_sentence_size))
    model.add(Flatten())
    for activation_fun in activations_functions:
        model.add(Dense(1, activation=activation_fun))
        if len(dropouts) > 0 and dropouts[0] > 0:
            model.add(Dropout(dropouts.pop(0)))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    model.fit(texts_train, labels_train, epochs=epochs, verbose=verbose, batch_size=batch_size)
    if verbose:
        print(model.summary())
    return model

def get_data_to_predict(texts, vocab_length, max_sentence_size):
    texts = list(map(lambda sentence : sentence if len(word_tokenize(sentence)) <= max_sentence_size else \
    " ".join(word_tokenize(sentence)[0:max_sentence_size]), texts))
    coded_sentences = list(map(lambda sentence : one_hot(sentence, vocab_length), texts))
    
    return pad_sequences(coded_sentences, max_sentence_size, padding='post')

def get_predictions(texts, model, vocab_length, max_sentence_size):
    to_predict = get_data_to_predict(texts, vocab_length, max_sentence_size)
    preds = model.predict(to_predict)
    
    return preds

# -- ==user_accounts== --