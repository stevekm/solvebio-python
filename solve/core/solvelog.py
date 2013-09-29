import logging
import os

# TODO: put these in SolveConfig
LOGLEVEL_STREAM = os.environ.get('SOLVE_LOGLEVEL_STREAM', 'WARNING')
LOGLEVEL_FILE = os.environ.get('SOLVE_LOGLEVEL_FILE', 'WARNING')


def _init_logging():
    base_logger = logging.getLogger("solve")
    base_logger.setLevel('DEBUG')

    #clear handlers if any exist
    handlers = base_logger.handlers[:]
    for handler in handlers:
        base_logger.removeHandler(handler)
        handler.close()

    if LOGLEVEL_STREAM:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(LOGLEVEL_STREAM)
        stream_fmt = logging.Formatter('[Solve] %(message)s')
        stream_handler.setFormatter(stream_fmt)
        base_logger.addHandler(stream_handler)

    if LOGLEVEL_FILE:
        logfile_path = os.path.expanduser('~/.solve/solve.log')
        if not os.path.isdir(os.path.dirname(logfile_path)):
            os.makedirs(os.path.dirname(logfile_path))

        file_handler = logging.FileHandler(logfile_path)
        file_handler.setLevel(LOGLEVEL_FILE)
        file_fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_fmt)
        base_logger.addHandler(file_handler)

    base_logger.addHandler(logging.NullHandler())
    return base_logger

solvelog = _init_logging()
