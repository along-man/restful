"""
    created by along on 2025.03.29
"""
from flask import json, request
from wtforms import Form
from app.libs.error_code import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.json
        super(BaseForm, self).__init__(data=data)

    # 重写Form的validate方法，使其能够抛出异常?
    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # form errors
            raise ParameterException(msg=self.errors)
        return self