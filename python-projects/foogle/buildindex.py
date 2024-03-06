import re


class BuildIndex:
    def __init__(self, files):
        self.filenames = files
        self.file_to_terms = self.process_files()
        self.term_indices = self.make_indices(self.file_to_terms)
        self.total_index = self.full_index()

    def process_files(self):
        file_to_terms = {}
        for file in self.filenames:
            pattern = re.compile(r'[\W_]+')
            file_to_terms[file] = open(file, 'r').read().lower()
            file_to_terms[file] = pattern.sub(' ', file_to_terms[file])
            re.sub(r'[\W_]+', '', file_to_terms[file])
            file_to_terms[file] = file_to_terms[file].split()
        return file_to_terms

    @staticmethod
    def index_one_file(term_list):
        file_index = {}
        for index, word in enumerate(term_list):
            if word in file_index.keys():
                file_index[word].append(index)
            else:
                file_index[word] = [index]
        return file_index

    def make_indices(self, term_lists):
        total = {}
        for filename in term_lists.keys():
            total[filename] = self.index_one_file(term_lists[filename])
        return total

    def full_index(self):
        total_index = {}
        indie_indices = self.term_indices
        for filename in indie_indices.keys():
            for word in indie_indices[filename].keys():
                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        total_index[word][filename].extend(
                            indie_indices[filename][word][:])
                    else:
                        total_index[word][filename] = \
                            indie_indices[filename][word]
                else:
                    total_index[word] = \
                        {filename: indie_indices[filename][word]}
        return total_index
