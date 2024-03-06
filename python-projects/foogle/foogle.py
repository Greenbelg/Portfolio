import shlex
from pathlib import Path
from printer import Printer
from querytext import Query
from ranging import RangingType
from syntax_tree import SyntaxTree

root_catalog = Path(__file__).parent
query = None


def find_docs_for_operand_not(value):
    global query
    docs = find_documents_with_rangs(value)
    not_zero_rang_files = [doc.file for doc in docs] if docs else []
    docs = [RangingType(1 / (len(query.filenames) - len(not_zero_rang_files)),
                        file)
            for file in query.filenames
            if file not in not_zero_rang_files]
    return docs[::-1]


def find_docs_for_operand_and(values):
    docs1 = find_documents_with_rangs(values[0])
    docs2 = find_documents_with_rangs(values[1])
    if not docs1 or not docs2:
        return []
    return sorted([RangingType(
        (doc1.rang + doc2.rang) / 2, doc1.file)
        for doc1 in docs1 for doc2 in docs2
        if doc1.file == doc2.file],
        key=lambda doc: doc.rang)


def find_docs_for_operand_or(values):
    docs1 = find_documents_with_rangs(values[0])
    docs2 = find_documents_with_rangs(values[1])
    if not docs1 or not docs2:
        return docs1 if docs1 else docs2 if docs2 else []

    result = {}
    for doc1 in docs1:
        if doc1.file not in result:
            result[doc1.file] = []
        result[doc1.file].append(doc1.rang)
        for doc2 in docs2:
            if doc2.file not in result:
                result[doc2.file] = []
            result[doc2.file].append(doc2.rang)

    result = {key: max(values) for key, values in result.items()}

    return sorted([RangingType(rang, file) for file, rang in result.items()],
                  key=lambda doc: doc.rang)


def find_documents_with_rangs(node):
    if value := SyntaxTree.try_get_value(node):
        return query.phrase_query(value)

    if value := SyntaxTree.try_get_operand_not(node):
        return find_docs_for_operand_not(value)

    if values := SyntaxTree.try_get_operands_and(node):
        return find_docs_for_operand_and(values)

    if values := SyntaxTree.try_get_operands_or(node):
        return find_docs_for_operand_or(values)


def has_text_data(file_path: Path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return True
    except UnicodeDecodeError:
        return False
    except Exception as e:
        return False


def get_text_files_from_catalog(path_to_catalog):
    catalog = root_catalog.joinpath(path_to_catalog)
    result = []
    try:
        for item in catalog.iterdir():
            if item.is_file() and has_text_data(item):
                result.append(item)
            elif item.is_dir():
                result.extend(get_text_files_from_catalog(
                    str(Path(path_to_catalog).joinpath(item.name))))
        return result
    except FileNotFoundError:
        Printer.print_path_not_found()


def main():
    global query
    Printer.print_welcome()
    while True:
        try:
            input_string = shlex.split(input())
        except ValueError:
            Printer.print_wrong_entered_data()
            continue
        if not input_string or \
                input_string[0] not in ['indexing', 'search'] or \
                len(input_string) < 2:
            Printer.print_wrong_entered_data()
            continue

        if input_string[0] == 'indexing':
            files_in_catalog = get_text_files_from_catalog(input_string[1])
            if files_in_catalog:
                query = Query(files_in_catalog)
            continue

        if not query:
            Printer.print_catalog_is_empty()
            continue

        query_tree = SyntaxTree().build(input_string[1:])
        if query_tree == -1:
            Printer.print_wrong_entered_data()
            continue

        docs = [doc.file for doc in find_documents_with_rangs(
            query_tree.get_first_expression())]
        Printer.print_results(docs)


if __name__ == '__main__':
    main()
