import logging.config
from logging.handlers import RotatingFileHandler

import yaml

from app.functions import app


def exception(e, *args, **kwargs):
    app.logger.exception(e, *args, **kwargs)


def error(error_message, *args, **kwargs):
    app.logger.error(error_message, *args, **kwargs)


def info(info_message, *args, **kwargs):
    app.logger.info(info_message, *args, **kwargs)


def init_loggers():
    yaml.warnings({'YAMLLoadWarning': False})
    logging.config.dictConfig(yaml.load(open('logging.conf')))
    log_console = logging.getLogger('console')
    log_file = logging.getLogger('file')

    try:
        for handler in log_file.handlers[:]:
            log_file.removeHandler(handler)
        file_handler = RotatingFileHandler('logs/console.log', maxBytes=5000000, backupCount=10)
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        file_handler.setLevel('INFO')
        log_file.addHandler(file_handler)
        log_file.propagate = False
        logging.root.addHandler(file_handler)
    except Exception as e:
        log_console.exception('server setup exception: %s', e)
    finally:
        log_console.debug("--Log Debug In Console Ready--")