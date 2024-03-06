import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
file_path_texts = Path(__file__).parent.joinpath("texts_for_tests")

from foogle import \
    find_docs_for_operand_or, find_docs_for_operand_and, \
    find_docs_for_operand_not, \
    has_text_data, get_text_files_from_catalog
from ranging import RangingType


class TestFoogle(unittest.TestCase):
    def setUp(self):
        self.files = [file_path_texts.joinpath('file1.txt'),
                      file_path_texts.joinpath('file2.txt')]

    @patch('foogle.find_documents_with_rangs',
           return_value=[RangingType(0.8,
                                     file_path_texts.joinpath('file1.txt'))])
    @patch('foogle.query')
    def test_find_docs_for_operand_not(self, query, find_docs):
        query.filenames = self.files
        result = find_docs_for_operand_not("some_value")
        expected_result = file_path_texts.joinpath('file2.txt')
        self.assertEqual(result[-1].file, expected_result)

    def test_find_docs_for_operand_and(self):
        with patch('foogle.find_documents_with_rangs',
                   return_value=[RangingType(0.5, self.files[0])]):
            result = find_docs_for_operand_and(["value1", "value2"])
            self.assertEqual(result[-1].file, self.files[0])

        with patch('foogle.find_documents_with_rangs',
                   side_effect=[[RangingType(0.5, file)
                                 for file in self.files[:2]],
                                [RangingType(0.7, file)
                                 for file in self.files[1:]]]):
            result = find_docs_for_operand_and(["value1", "value2"])
            expected_result = [file for file in self.files[1:]]
            self.assertEqual([doc.file for doc in result], expected_result)

    def test_find_docs_for_operand_or(self):
        with patch('foogle.find_documents_with_rangs',
                   return_value=[RangingType(0.5, self.files[0])]):
            result = find_docs_for_operand_or(["value1", "value2"])
            self.assertEqual(result[-1].file, self.files[0])

        with patch('foogle.find_documents_with_rangs',
                   side_effect=[[RangingType(0.5, file)
                                 for file in self.files[:1]],
                                [RangingType(0.7, file)
                                 for file in self.files[1:]]]):
            result = find_docs_for_operand_or(["value1", "value2"])
            expected_result = [file for file in self.files[0:]]
            self.assertEqual([doc.file for doc in result], expected_result)

    def test_has_text_data(self):
        text_data_file = file_path_texts.joinpath('file1.txt')
        not_text_data_file = file_path_texts.joinpath('not_text_file.gif')

        self.assertTrue(has_text_data(text_data_file))
        self.assertFalse(has_text_data(not_text_data_file))

    def test_get_text_files(self):
        files = get_text_files_from_catalog(file_path_texts)
        nothing = get_text_files_from_catalog(file_path_texts.joinpath('aaa'))
        expected = ['file2.txt', 'file1.txt',
                    'short_file_for_test_helper_classes',
                    'short_story.txt', 'file42.txt']
        results = [file.name for file in files]

        self.assertIsNone(nothing)
        self.assertListEqual(sorted(expected), sorted(results))


if __name__ == '__main__':
    unittest.main()
