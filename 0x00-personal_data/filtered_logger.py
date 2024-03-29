#!/usr/bin/env python3
"""
Regex-ing ->
    function = filter_datum -> returns log message obfuscated
    The function uses regex to replace the equivalent\
     of items in the fields list
"""
from typing import List
import re
import os
import logging
import mysql.connector


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connection to MySQL environment """
    db_connect = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connect


def get_logger() -> logging.Logger:
    """create a logger named user_data and sends output to the console
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    target_handler = logging.StreamHandler()
    target_handler.setLevel(logging.INFO)

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


def main():
    """
    gets rows from db
    """
    db = get_db()
    if db.is_connected():
        query = "SELECT * FROM users;"
        cursor = connection.cursor()

        cursor.execute(query)

        headers = [field[0] for field in cursor.description]
        logger = get_logger()

        for row in cursor:
            info_answer = ''
            for f, p in zip(row, headers):
                info_answer += f'{p}={(f)}; '
            logger.info(info_answer)

        cursor.close()
        db.close()

if __name__ == "__main_":
    main()