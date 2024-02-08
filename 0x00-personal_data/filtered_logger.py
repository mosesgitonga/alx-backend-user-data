#!/usr/bin/env python3
"""
Regex-ing ->
    function = filter_datum -> returns log message obfuscated
    The function uses regex to replace the equivalent\
     of items in the fields list
"""
from typing import List
import re


import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        returns record with a format from  given record
        """
        message = super().format(record)
        formated_msg = filter_datum(self.fields,
                                    self.REDACTION,
                                    message,
                                    RedactingFormatter.SEPARATOR)
        return formated_msg


PII_FIELDS = ('name', 'email', 'ssn', 'password',
              'ip', 'last_login', 'user_agent')


def get_logger() -> logging.Logger:
    """create a logger named user_data and sends output to the console
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propergate = False

    target_handler = logging.StreamHandler()
    target_handler.setLevel(logging.info)

    formatter = RedactingFormatter(list(PII_FIELDS))
    target_handler.setFormatter(formatter)

    logger.addHandler(target_handler)
    return logger


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """return regex obfuscated messages"""
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message
