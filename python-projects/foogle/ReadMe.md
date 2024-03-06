#Ппоисковой движок "Foogle"

Авторы: Володько Екатерина, Моськов Алексей


## Описание
Поисковой движок над локальными файлами (только текстовые)


## Требования
* Python версии 3
* Requirements


## Состав
* Обработка событий: `foogle.py`
* Нахождение файлов с рангом: `querytext.py`
* Ранжирование: `ranging.py`
* Построение индекса: `buildindex.py`
* Релевантность: `define_frequencies.py`
* Вывод информации: `printer.py`
* Парсинг запроса: `syntax_tree.py`
* Тесты `tests/`
* Локальные файлы: `files/`


## Консольная версия
Пример запуска: `foogle.py`

Команды:
* `indexing <path/to/catalog>` - индексирование каталога `<path/to/catalog>`
* `search [NOT] <"words sequence"> [[AND|OR] [NOT] <"words sequence">]*` - поиск запроса
