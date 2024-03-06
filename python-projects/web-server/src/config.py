from pathlib import Path


class CODES:
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404


class EVENT_TYPES:
    INCOMING = 'incoming_connection'


SERVER_HOST = '127.0.0.1'
PORTS = [12345, 12346]

HOSTS = {12345: 'alex.com',
         12346: 'kate.com',
        }

STATES_CODES = {200: b"OK",
                400: b"Bad Request",
                404: b"Not Found",
               }

HEADERS = {
    # header: value,
    # ...
}

ACCEPT_DATA_IN_BYTES = 1024

PATH_TO_LOGS = Path(__file__).parent.parent.joinpath('logs').joinpath('webserver.log')

MAX_LOG_IN_BYTES = 1024 ** 2

LOG_BACKUP_COUNT = 5

LOGGER_FILE = 'my_webserver'

LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

CRLF = '\r\n'