#!/usr/bin/env python3
"""filtering loggs"""
import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """filteing data and hiandeling redactions"""
    for field in fields:
        reg = f"{field}=[^{separator}]*"
        message = re.sub(reg, f"{field}={redaction}", message)
    return message


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
        """filtering"""
        msg = record.msg
        msg = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        record.msg = msg
        return super().format(record)


def get_logger() -> logging.Logger:
    """Return a logging.Logger object named 'user_data'."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


PII_FIELDS = ('name', 'email', 'phone', 'address', 'credit_card_number')


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a connector to the database
    (mysql.connector.connection.MySQLConnection object).
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    db = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
    return db

def main():
    """Retrieve all rows in the users table and display each row under a filtered format."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        logger.info("name=%s; email=%s; phone=%s; ssn=%s; password=%s; ip=%s; last_login=%s; user_agent=%s;",
                    row['name'], row['email'], row['phone'], row['ssn'], row['password'], row['ip'], row['last_login'], row['user_agent'])
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
