#!/usr/bin/env python3
"""
Regex-ing ->
    function = filter_datum -> returns log message obfuscated
    The function uses regex to replace the equivalent\
     of items in the fields list
"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """return regex obfuscated messages"""
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message
