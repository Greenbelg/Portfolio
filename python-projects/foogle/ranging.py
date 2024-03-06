import re

from define_frequencies import FrequenciesFinder


class RangingType:
    def __init__(self, rang, file):
        self.rang = rang
        self.file = file


class Ranger:
    def __init__(self, filenames):
        self.filenames = filenames
        self.frequencies_finder = FrequenciesFinder(filenames)
        self.index = self.frequencies_finder.index

    def make_query_vector(self, query):
        pattern = re.compile(r'[\W_]+')
        query = pattern.sub(' ', query)
        split_query = query.split()
        query_vec = [0] * len(split_query)
        index = 0
        for ind, word in enumerate(split_query):
            query_vec[index] = self.define_query_freq(word, query)
            index += 1
        query_idf = [self.frequencies_finder.idf[word]
                     for word in self.index.total_index.keys()]
        magnitude = pow(sum(map(lambda x: x ** 2, query_vec)), .5)
        freq = self.make_terms_freq(self.index.total_index.keys(), query)
        tf = [x / magnitude for x in freq]
        final = [tf[i] * query_idf[i]
                 for i in range(len(self.index.total_index.keys()))]
        return final

    @staticmethod
    def define_query_freq(term, query):
        count = 0
        for word in query.split():
            if word == term:
                count += 1
        return count

    def make_terms_freq(self, terms, query):
        temp = [0] * len(terms)
        for i, term in enumerate(terms):
            temp[i] = self.define_query_freq(term, query)
        return temp

    @staticmethod
    def dot_product(doc1, doc2):
        if len(doc1) != len(doc2):
            return 0
        return sum([x * y for x, y in zip(doc1, doc2)])

    def rang_results(self, files, query):
        files_vectors = self.frequencies_finder.vectors
        query_vector = self.make_query_vector(query)
        results = [[self.dot_product(files_vectors[result], query_vector),
                    result]
                   for result in files]
        results.sort(key=lambda x: x[0], reverse=True)
        results = [RangingType(x[0], x[1]) for x in results]
        return results
