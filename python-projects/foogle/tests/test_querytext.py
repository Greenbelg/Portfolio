import os
import pathlib
import sys
import unittest

from querytext import Query

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
file_path_texts = pathlib.Path(__file__).parent.joinpath("texts_for_tests")
q = Query([file_path_texts.joinpath('file1.txt'),
           file_path_texts.joinpath('file2.txt')])


class QueryTexts(unittest.TestCase):
    def test_free_text_query(self):
        phrases = ['Irish wristwatch', 'witch wished',
                   'two witches', 'wish the wish', 'wicked wish',
                   'wish the witch wishes', 'afraid of witches',
                   'one task', 'two gold watches',
                   'wish the witch wish']
        expected_results = [['file1.txt'],
                            ['file1.txt', 'file2.txt'],
                            ['file2.txt', 'file1.txt'],
                            ['file2.txt', 'file1.txt'],
                            ['file1.txt', 'file2.txt'],
                            ['file2.txt', 'file1.txt'],
                            ['file1.txt', 'file2.txt'],
                            [],
                            ['file2.txt'],
                            ['file2.txt', 'file1.txt']]
        for i in range(len(phrases)):
            result = [os.path.basename(item.file)
                      for item in q.free_text_query(phrases[i])]
            self.assertEqual(result, expected_results[i])

    def test_one_word_query(self):
        words = ['witch', 'irish', 'one',
                 'two', 'watching', 'wish',
                 'you', 'afraid', 'wristwatch',
                 'test', 'python', 'code']
        expected_results = [['file1.txt', 'file2.txt'], ['file1.txt'], [],
                            ['file2.txt'], ['file2.txt'],
                            ['file1.txt', 'file2.txt'], ['file2.txt'],
                            ['file1.txt'], ['file1.txt'], [], [], []]
        for i in range(len(words)):
            result = [os.path.basename(item.file)
                      for item in q.one_word_query(words[i])]
            self.assertEqual(result, expected_results[i])

    def test_phrase_query(self):
        phrases = ['Irish wristwatch', 'witch wished',
                   'two witches', 'wish the wish', 'wicked wish',
                   'wish the witch wishes', 'afraid of witches',
                   'one task', 'frightening witch']
        expected_results = [['file1.txt'], ['file1.txt'], ['file2.txt'],
                            ['file2.txt'], ['file1.txt'], ['file2.txt'],
                            ['file1.txt'], [], []]
        for i in range(len(phrases)):
            result = [os.path.basename(item.file)
                      for item in q.phrase_query(phrases[i])]
            self.assertEqual(result, expected_results[i])
