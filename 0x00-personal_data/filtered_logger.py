#!/usr/bin/env python3
"""These code will implement logger
"""
import os
import re
import logging
from typing import List
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log messages which is obfuscated"""
    for field in fields:
        pattern = re.escape('{}='.format(field))
        message = re.sub('{}[^{}]+'.format(pattern, separator),
                         '{}={}'.format(field, redaction), message,
                         flags=re.IGNORECASE)
    return message


class RedactingFormatter(logging.Formatter):
    """This class Redacting to Formatter"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """intialize"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """customized messege will be returned"""
        formated = filter_datum(self.fields, self.REDACTION,
                                record.msg, self.SEPARATOR)
        record.msg = formated
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """returns obeject which is logging.Logger"""

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    redacting_formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(redacting_formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""

    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(host=db_host,
                                         user=db_user,
                                         password=db_pwd,
                                         database=db_name)

    return connection


def main():
    """
    the code starts executing from here
    """
    logger = get_logger()
    db_conn = get_db()
    cursor = db_conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        row_string = ";".join(["{}={}".format(key, value)
                              for key, value in row.items()])
        logger.info(row_string)

    cursor.close()
    db_conn.close()


if __name__ == "__main__":
    main()
