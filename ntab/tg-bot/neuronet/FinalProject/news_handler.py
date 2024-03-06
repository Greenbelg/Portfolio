import pickle
import pymorphy3
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
from keras.models import load_model
from pathlib import Path


class NewsHandler:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self._punctuation_marks = ['!', ',', '(', ')', ':', '-', '?', '.', '..', '...', ';', '--', 'https', 'http', '|',
                                   '//t.me/kpekp_news', '//t.me/kpekb', '[', ']', '@', '//t.me/ekat01',
                                   '//t.me/ekat01_bot',
                                   '//t.me/+tb5-xbiawtlqmxey', '//t.me/+m4yuxq2p5w8ymjri', '//t.me/ekb4tv', "''", '``']
        self._stop_words = stopwords.words("russian")
        self._morph = pymorphy3.MorphAnalyzer()
        with open(Path(__file__).parent.joinpath('word_to_index.pkl'), 'rb') as f:
            self._word_to_index = pickle.load(f)
        with open(Path(__file__).parent.joinpath('index_to_word.pkl'), 'rb') as f:
            self._index_to_word = pickle.load(f)
        self._max_words = 10000

    def _preprocess(self, text, stop_words, punctuation_marks, morph):
        if pd.isnull(text):
            return ''
        tokens = word_tokenize(text.lower())
        preprocessed_text = []
        for token in tokens:
            if token not in punctuation_marks:
                lemma = morph.parse(token)[0].normal_form
                if lemma not in stop_words:
                    preprocessed_text.append(lemma)
        return preprocessed_text

    def _text_to_sequence(self, txt, word_to_index):
        seq = []
        for word in txt:
            index = word_to_index.get(word, 1)  # 1 означает неизвестное слово
            # Неизвестные слова не добавляем в выходную последовательность
            if index != 1:
                seq.append(index)
        return seq

    def return_result(self, news):
        preprocessed_news = self._preprocess(news, self._stop_words, self._punctuation_marks, self._morph)
        sequence_news = self._text_to_sequence(preprocessed_news, self._word_to_index)
        max_review_len = 100
        x = pad_sequences([sequence_news], max_review_len)
        model = load_model(Path(__file__).parent.joinpath('best_model.h5'))
        Y_predicted = model.predict(x)
        if Y_predicted[[0]] < 0.5:
            print("Не связано с дтп")
            return True
        print("Связано с дтп")
        return False
