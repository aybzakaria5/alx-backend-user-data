#!/usr/bin/env python3
"""filtering loggs"""
import re


def filter_datum(fields, redaction, message, separator):
    """filteing data and handeling redactions"""
    for field in fields:
        reg = f"{field}=[^{separator}]*"
        message = re.sub(reg, f"{field}={redaction}", message)
    return message
