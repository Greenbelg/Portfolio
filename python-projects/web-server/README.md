# Веб-сервер "web-server"
Версия 1.1

Авторы: Володько Екатерина, Моськов Алексей

## Описание
Реализован простой веб-сервер, который стартует на localhost и слушает порты 12345, 12346.
В файле конфигурации можно задать host и порты.
Поддерживает HTTP-метод GET.


## Требования
* Python версии 3
* Установленные библиотеки из requirements.txt


## Состав
* Веб-сервер: `server.py`
* Обработка запросов: `src/request_handler.py`
* Реализация паттерна "реактор": `src/reactor.py`
* Задание формата логирования: `src/logger.db`
* Класс, реализующий сборку HTTP-ответа: `src/HTTPResponse.py`
* Класс, реализующий разбор HTTP-запроса: `src/HTTPRequest.py`
* Файл конфигурации: `src/config.py`
* Хосты: `www/`
* Файлы с результатами логирования: `logs/`
* Тесты: `tests/`


## Запуск сервера
Пример запуска: `python server.py`


## Подробности реализации
* При создании сервера реализован паттерн reactor - `src/reactor.py`.
* Сервер слушает порты 12345, 12346 - по умолчанию. 
* В файле конфигурации можно корректировать работу логера, слушаемые порты, адрес сервера, добавлять сайты.
* По умолчанию на 12345 порту расположен `alex.com`, на 12346 - `kate.com`
* При поступлении запроса разбирается только его заголовок, остальной разбор происходит по мере необходимости.