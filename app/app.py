"""
    created by along on 2025.03.18
"""
from datetime import date
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.libs.error_code import SeverError


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(0, date):
            return o.strftime('')
        raise SeverError()

class Flask(_Flask):
    json_encoder = JSONEncoder



