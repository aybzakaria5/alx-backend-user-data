#!/usr/bin/env python3
"""filtering loggs"""
import re


def filter_datum(fields, redaction, message, separator):
    """filteing data and handeling redactions"""
    pattern = (
        fr'((?:^|{re.escape(separator)})(?:{"|".join(fields)})=)'
        fr'[^{separator}]*(?={re.escape(separator)}|$)'
    )
    return re.sub(pattern, fr'\1{redaction}', message)
