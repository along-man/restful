from app.libs.error import APIException


class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0

class DeleteSuccess(Success):
    code = 202
    msg = 'delete success'
    error_code = 1

# 服务器内部错误
class SeverError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)'
    error_code = 999

# 无效的客户端类型
class ClientTypeError(APIException):
    code = 400
    msg = 'invalidate client type'
    error_code = 1006

# 参数错误 ?
class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000

# 资源没找到
class NotFound(APIException):
    code = 404
    msg = 'the resource are not found 0__0...'
    error_code = 1001

# 授权失败
class AuthFailed(APIException):
    code = 401
    msg = 'authorization failed'
    error_code = 1004