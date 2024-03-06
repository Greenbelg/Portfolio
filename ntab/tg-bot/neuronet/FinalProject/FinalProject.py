import pickle
import pymorphy3
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from keras.utils import pad_sequences
import pandas as pd
from keras.models import load_model


#Скачивание данных (необходимо только 1 раз)
'''
nltk.download('punkt')
nltk.download('stopwords')
'''

#Текст
news = "Сбили кролика на дороге"

#Подготовка текста
def preprocess(text, stop_words, punctuation_marks, morph):
    if pd.isnull(text): return ''
    tokens = word_tokenize(text.lower())
    preprocessed_text = []
    for token in tokens:
        if token not in punctuation_marks:
            lemma = morph.parse(token)[0].normal_form
            if lemma not in stop_words:
                preprocessed_text.append(lemma)
    return preprocessed_text

punctuation_marks = ['!', ',', '(', ')', ':', '-', '?', '.', '..', '...', ';', '--', 'https', 'http', '|', '//t.me/kpekp_news', '//t.me/kpekb', '[', ']', '@', '//t.me/ekat01', '//t.me/ekat01_bot', '//t.me/+tb5-xbiawtlqmxey', '//t.me/+m4yuxq2p5w8ymjri', '//t.me/ekb4tv', "''", '``']
stop_words = stopwords.words("russian")
morph = pymorphy3.MorphAnalyzer()

preprocessed_news = preprocess(news, stop_words, punctuation_marks, morph)

#Загрузка словарей
with open('word_to_index.pkl', 'rb') as f:
    word_to_index = pickle.load(f)
with open('index_to_word.pkl', 'rb') as f:
    index_to_word = pickle.load(f)

max_words = 10000

def text_to_sequence(txt, word_to_index):
    seq = []
    for word in txt:
        index = word_to_index.get(word, 1) # 1 означает неизвестное слово
        # Неизвестные слова не добавляем в выходную последовательность
        if index != 1:
            seq.append(index)
    return seq

sequence_news = text_to_sequence(preprocessed_news, word_to_index)


#TIME TO НЕЙРОНКА

num_words = 10000
max_review_len = 100
x = pad_sequences([sequence_news], max_review_len)
model = load_model("best_model.h5")
Y_predicted = model.predict(x)

def return_result(Y):
    print(Y[[0]])
    if Y[[0]] < 0.5:
        print("Не связано с дтп")
        return True
    print("Связано с дтп")
    return False
return_result(Y_predicted)