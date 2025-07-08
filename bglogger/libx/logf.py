import os, sys
import logging
from datetime import datetime


CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


# Полезные форматы logging.Formatter
# ---
# - %(asctime)s   — время события
# - %(levelname)s — уровень (DEBUG, INFO, ERROR и т.п.)
# - %(message)s   — сообщение
# - %(name)s      — имя логгера
# - %(filename)s  — имя файла вызова
# - %(lineno)d    — номер строки

# https://docs.python.org/2/library/logging.html?highlight=msec#logrecord-attributes
# format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# format = logging.Formatter("[%(levelname)-8s] %(message)s")

DATEFMT_SHORT = '%Y%m%d %H:%M:%S'
DATEFMT_FULL = '%Y-%m-%d %H:%M:%S'


def get_line_formatter(asctime=True, msecs=False, name=False
                        , process=False, processid=False
                        , level=True, thread=False, threadid=False
                        , module=False, lineno=False
                        , datefmt=None):
    '''
    Возвращает форматтер с указанными параметрами
    '''
    datefmt = datefmt or "%Y-%m-%d %H:%M:%S"

    fmt = []
    if asctime:
        ms = ",%(msecs)03d" if msecs else ""
        t = f"%(asctime)s{ms}"
        fmt.append(t)
    if name:
        fmt.append("%(name)s")
    if process:
        fmt.append("%(processName)s")
    if processid:
        fmt.append("[%(process)d]")
    if level:
        fmt.append("%(levelname)-5s")
    if thread:
        fmt.append("[%(threadName)s]")
    if threadid:
        fmt.append("[%(thread)d]")
    if module:
        fmt.append("%(module)s")
    if lineno:
        fmt.append("st. %(lineno)d")

    fmt.append("%(message)s")
    format = " ".join(fmt)

    return logging.Formatter(format, datefmt)


def get_message_only_formatter():
    '''
    Возвращает форматтер, в котором выводится только текстовое сообщение
    '''
    return logging.Formatter("%(message)s")


def get_console_handler(formatter=None, level=None):
    handler = logging.StreamHandler() #stream=sys.stdout)
    handler.setFormatter(fmt=formatter)
    if level:
        handler.setLevel(level)
    return handler


def get_file_handler(logfile, mode="w", formatter=None, level=None):
    handler = logging.FileHandler(logfile, mode=mode, encoding="UTF-8", errors="ignore")
    handler.setFormatter(fmt=formatter)
    if level:
        handler.setLevel(level)
    return handler


def split_path(filepath: str):
    '''
    Разделяет переданную строку на название директории, имя файла и расширение
    '''
    if not filepath:
        raise ValueError('Необходимо указать путь к файлу')

    dirname, filename = os.path.split(filepath)
    dirname = os.path.normpath(dirname) if dirname else ''

    filename = filename.strip()
    if not filename:
        raise ValueError('Некорректное имя файла')

    name, ext = os.path.splitext(filename)
    name = name.strip(' \r\n\t.-_')
    if not name:
        raise ValueError('Некорректное имя файла')

    return dirname, name, ext


def get_date_formatter(date: datetime|str|None=None, pattern=''):
    date = date or datetime.now()
    pattern = pattern or "%Y-%m-%d_%H-%M-%S"
    if isinstance(date, str):
        date = datetime.strptime(date, pattern)

    def format(bf, output_pattern=''):
        output_pattern = output_pattern or pattern
        snow = date.strftime(output_pattern)
        return f"{bf}_{snow}"

    return format


def get_version_formatter(version):
    if not version:
        raise ValueError('version: ожидалась версия, типа 1.2.3 и т.п.')

    version = version.strip()

    def format(bf):
        return f'{bf}_{version}'
    return format


def prepare_logname(basename: str, formatter=None):
    dirname, logname, _ = split_path(basename)
    if formatter:
        if not callable(formatter):
            raise ValueError('formatter: ожидалась функция или callable объект')
        logname = str(formatter(logname))
    
    if dirname:
        logname = os.path.join(dirname, logname)
    return logname + '.log'

def prepare_logname_tm(basename: str):
    formatter = get_date_formatter()
    return prepare_logname(basename, formatter)

def prepare_logname_ver(basename: str, version: str):
    formatter = get_version_formatter(version)
    return prepare_logname(basename, formatter)


