import os
import pathlib
import sys
import unittest

from buildindex import BuildIndex
from ranging import Ranger

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
file_path_texts = pathlib.Path(__file__).parent.joinpath("texts_for_tests")


class HelperClassesTests(unittest.TestCase):
    def test_build_index_methods(self):
        build_index = BuildIndex(
            [file_path_texts.joinpath('short_file_for_test_helper_classes')])
        expected_total_index = [
            {'i': {'short_file_for_test_helper_classes': [0]}},
            {'wish': {'short_file_for_test_helper_classes': [1]}},
            {'to': {'short_file_for_test_helper_classes': [2]}},
            {'wash': {'short_file_for_test_helper_classes': [3]}},
            {'my': {'short_file_for_test_helper_classes': [4]}},
            {'irish': {'short_file_for_test_helper_classes': [5]}},
            {'wristwatch': {'short_file_for_test_helper_classes': [6]}}]
        expected_term_indices = {
            'short_file_for_test_helper_classes':
                {'i': [0], 'wish': [1], 'to': [2], 'wash': [3],
                 'my': [4], 'irish': [5], 'wristwatch': [6]}}
        total_index = []
        for term, data in build_index.total_index.items():
            data = {os.path.basename(k): v for k, v in data.items()}
            total_index.append({str(term): data})
        self.assertEqual(total_index, expected_total_index)
        term_indices = {os.path.basename(file): data
                        for file, data in build_index.term_indices.items()}
        self.assertEqual(term_indices, expected_term_indices)

    def test_ranging_results(self):
        files = [file_path_texts.joinpath(
                    'short_file_for_test_helper_classes'),
                 file_path_texts.joinpath('file1.txt'),
                 file_path_texts.joinpath('file2.txt'),
                 file_path_texts.joinpath('short_story.txt')]
        ranger = Ranger(files)
        searching_phrases = ['two witches', 'afraid of witches']
        expected_results = ['file2.txt', 'file1.txt',
                            'short_story.txt',
                            'short_file_for_test_helper_classes',
                            'file1.txt', 'file2.txt', 'short_story.txt',
                            'short_file_for_test_helper_classes']
        result = [os.path.basename(res.file)
                  for search_phrase in searching_phrases
                  for res in ranger.rang_results(files, search_phrase)]
        self.assertEqual(result, expected_results)
