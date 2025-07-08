import os
import libx.logf as logf
from libx.bglogger import BackgroundLogger


def configure_logger(log_file, level=logf.DEBUG):
    fmt = logf.get_line_formatter(datefmt=logf.DATEFMT_SHORT)

    console_handler = logf.get_console_handler(fmt, level)
    file_handler = logf.get_file_handler(log_file, 'a', fmt, level)

    lg = BackgroundLogger(level=level)
    lg.addHandler(console_handler)
    lg.addHandler(file_handler)
    return lg




