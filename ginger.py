"""
    created by along on 2025.03.18
"""
from werkzeug.exceptions import HTTPException
from app import create_app
from app.libs.error import APIException
from app.libs.error_code import SeverError

app = create_app()

# ---------------------------
# 全局 AOP 错误处理层
# ---------------------------
@app.errorhandler(Exception)
def framework_errors(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        #log
        if not app.config['DEBUG']:
            return SeverError()
        else:
            raise e

if __name__ == '__main__':
    app.run(debug=False)
