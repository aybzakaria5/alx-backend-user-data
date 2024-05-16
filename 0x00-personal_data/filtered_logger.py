#!/usr/bin/env python3
"""filtering loggs"""
import re

def filter_datum(fields, redaction, message, separator):
    """filtering from a message """
    return re.sub(fr'((?:^|{re.escape(separator)})(?:{"|".join(fields)})=)[^{separator}]*(?={re.escape(separator)}|$)', fr'\1{redaction}', message)

