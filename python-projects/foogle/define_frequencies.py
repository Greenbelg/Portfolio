import math

import buildindex


class FrequenciesFinder:
    def __init__(self, filenames):
        self.filenames = filenames
        self.index = buildindex.BuildIndex(self.filenames)
        self.idf = {}
        self.tf = {}
        self.term_document_frequency = self.normalize_doc_term_frequency()
        self.term_frequency = self.define_term_frequency()
        self.vectors = self.make_files_vectors()

    def define_document_term_frequency(self):
        doc_term_frequency = {}
        for term in self.index.total_index.keys():
            for document in self.index.total_index[term].keys():
                doc_term_frequency.setdefault(document, {})[term] = \
                    len(self.index.total_index[term][document])
        return doc_term_frequency

    def normalize_doc_term_frequency(self):
        doc_term_frequency = self.define_document_term_frequency()
        for doc in doc_term_frequency.keys():
            len_doc = 0
            for _ in doc_term_frequency[doc].keys():
                len_doc += 1
            for terms in doc_term_frequency[doc].keys():
                doc_term_frequency[doc][terms] /= len_doc
        return doc_term_frequency

    def define_term_frequency(self):
        term_frequency = {}
        for term in self.index.total_index.keys():
            term_frequency[term] = 0
            for document in self.index.total_index[term].keys():
                if len(self.index.total_index[term][document]) > 0:
                    term_frequency[term] += 1
        return term_frequency

    def define_idf(self):
        for term in self.index.total_index.keys():
            self.idf[term] = \
                math.log(len(self.filenames) / self.term_frequency[term],
                         math.e)

    def make_files_vectors(self):
        self.define_idf()
        files_vectors = {}
        for file in self.filenames:
            file_vect = [0] * len(self.index.total_index.keys())
            for ind, term in enumerate(self.index.total_index.keys()):
                if term in self.term_document_frequency[file]:
                    file_vect[ind] = \
                        self.term_document_frequency[file][term] * \
                        self.idf[term]
            files_vectors[file] = file_vect
        return files_vectors
