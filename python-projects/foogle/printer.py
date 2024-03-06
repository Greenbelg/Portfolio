class Printer:
    @staticmethod
    def print_welcome():
        print('Foogle')
        print('Доступные команды:\n\r'
              'indexing <path/to/catalog>\n\r'
              'search [NOT] <"words sequence"> [[AND|OR] [NOT] <"words sequence">]*')

    @staticmethod
    def print_wrong_entered_data():
        print('Неправильный ввод, попробуйте снова\n\r'
              'Пример ввода:\n\r'
              'indexing files\n\r'
              'search "how are you" AND NOT "ok"')

    @staticmethod
    def print_path_not_found():
        print(
            'Данного каталога не существует,'
            'необходимо представить путь к каталогу от текущего')

    @staticmethod
    def print_catalog_is_empty():
        print('Сначала выберете каталог для индексирвания, '
              'в котором есть текстовые файлы')

    @staticmethod
    def print_results(docs):
        if not docs:
            print('Ничего не найдено')
            return

        print('Лучшее совпадение:')
        for doc in docs:
            print(doc)
