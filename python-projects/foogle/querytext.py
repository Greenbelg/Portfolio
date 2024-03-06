import re

from ranging import Ranger


class Query:
    def __init__(self, filenames):
        self.filenames = filenames
        self.ranger = Ranger(filenames)
        self.index = self.ranger.index
        self.inverted_index = self.index.total_index
        self.regular_index = self.index.term_indices

    def one_word_query(self, word):
        pattern = re.compile(r'[\W_]+')
        word = pattern.sub(' ', word)
        if word in self.inverted_index.keys():
            return self.ranger.rang_results(
                [filename for filename in self.inverted_index[word].keys()],
                word)
        else:
            return []

    def free_text_query(self, string):
        pattern = re.compile(r'[\W_]+')
        string = pattern.sub(' ', string.lower())
        result = []
        for word in string.split():
            result += [ranging_type.file
                       for ranging_type in self.one_word_query(word)]
        return self.ranger.rang_results(list(set(result)), string)

    def phrase_query(self, string):
        pattern = re.compile(r'[\W_]+')
        string = pattern.sub(' ', string.lower())
        word_to_files_mapping, result = [], []
        for word in string.split():
            word_to_files_mapping.append(
                [ranging_type.file
                 for ranging_type in self.one_word_query(word)])

        set_word_to_files_mapping = \
            set(word_to_files_mapping[0]).intersection(*word_to_files_mapping)
        for filename in set_word_to_files_mapping:
            temp = []
            for word in string.split():
                temp.append(self.inverted_index[word][filename][:])
            for j in range(len(temp)):
                for ind in range(len(temp[j])):
                    temp[j][ind] -= j
            if set(temp[0]).intersection(*temp):
                result.append(filename)
        return self.ranger.rang_results(result, string)
