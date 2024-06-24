# -*- coding: utf-8 -*-

"""
@Remark: 自定义异常处理
"""
from loguru import logger
import traceback
from rest_framework.exceptions import APIException as DRFAPIException, AuthenticationFailed, NotAuthenticated
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import set_rollback, exception_handler
from django.db.models import ProtectedError
from django.db.utils import DatabaseError
from flask import jsonify
from rest_framework import exceptions
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound
from utils.common.response import ErrorResponse


logger = logging.getLogger(__name__)

def CustomExceptionHandler(ex, context):
    """
    统一异常拦截处理
    目的:(1)取消所有的500异常响应,统一响应为标准错误返回
        (2)准确显示错误信息
    :param ex:
    :param context:
    :return:
    """
    msg = ''
    code = 4000
    if isinstance(ex, AuthenticationFailed):
        code = 4001
        if 'User is inactive' in str(ex.detail):
            msg = "该账号已被禁用,请联系管理员"
        else:
            msg = ex.detail
    elif isinstance(ex, NotAuthenticated):
        code = 4001
        msg = ex.detail
    # elif isinstance(ex,NotFound):
    #     if str(ex)=="无效页面。":
    #         msg="暂无数据"
    #     else:
    #         msg = str(ex)
    elif isinstance(ex, exceptions.ValidationError):
        msg = ex.detail
        errorMsg = msg
        try:
            for key in errorMsg:
                if key:
                    msg = '%s:%s' % (key, errorMsg[key][0])
                else:
                    msg = errorMsg[key][0]
        except:
            #{comment_author: {non_field_errors: ["无效数据。期待为字典类型，得到的是 str 。"]}, images: ["Not a valid string."]}
            if isinstance(errorMsg,list):
                msg = errorMsg[0]
            elif isinstance(errorMsg,dict):
                values_list = list(errorMsg.values())
                keys_list = list(errorMsg.keys())
                if 'non_field_errors' in values_list[0]:
                    msg = keys_list[0]+":"+values_list[0]['non_field_errors'][0]
                elif isinstance(values_list[0],list):
                    msg = keys_list[0]+":"+values_list[0][0]
                else:
                    msg = errorMsg[0]
            else:
                msg = errorMsg
    elif 'django.db.utils.IntegrityError' in str(type(ex)):
        msg=str(ex)
        res = msg.split(', ')
        if res[0] == '(1062':
            msg="数据有重复，请检查后重试:%s"%msg
    elif isinstance(ex,Http404):
        code = 404
        msg = "404错误：您访问的地址不存在"
    elif isinstance(ex, DRFAPIException):
        set_rollback()
        msg = str(ex.detail)
    elif isinstance(ex, exceptions.APIException):
        set_rollback()
        msg = ex.detail
    elif isinstance(ex, ProtectedError):
        set_rollback()
        msg = "删除失败:该条数据与其他数据有相关绑定"
    # elif isinstance(ex, DatabaseError):
    #     set_rollback()
    #     msg = "接口服务器异常,请联系管理员"
    elif isinstance(ex, Exception):
        logger.error(traceback.format_exc())
        msg = str(ex)#原样输出错误

    # errorMsg = msg
    # for key in errorMsg:
    #     msg = errorMsg[key][0]
    # print(traceback.format_exc())
    return ErrorResponse(msg=msg, code=code)


class APIException(Exception):
    """
    通用异常:(1)用于接口请求是抛出移除, 此时code会被当做标准返回的code, message会被当做标准返回的msg
    """

    def __init__(self, code=201, message='API异常', args=('API异常',)):
        self.args = args
        self.code = code
        self.message = message

    def __str__(self):
        return self.message
class ExceptionHandler:
    def __init__(self, app):
        self.app = app

    def handle_exception(self, e):
        # 可以在这里添加你的日志记录代码
        logger.error(f"An error occurred: {str(e)}")
        # 返回一个包含错误信息的 JSON 响应
        return jsonify({"error": str(e)}), 500

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except Exception as e:
            return self.handle_exception(e)



def CustomExceptionHandler(ex, context):
    """
    统一异常拦截处理
    目的:(1)取消所有的500异常响应,统一响应为标准错误返回
        (2)准确显示错误信息
    :param ex:
    :param context:
    :return:
    """
    msg = ''
    code = 4000
    # 调用默认的异常处理函数
    response = exception_handler(ex, context)
    if isinstance(ex, AuthenticationFailed):
        # 如果是身份验证错误
        if response and response.data.get('detail') == "Given token not valid for any token type":
            code = 401
            msg = ex.detail
        elif response and response.data.get('detail') == "Token is blacklisted":
            # token在黑名单
            return ErrorResponse(status=HTTP_401_UNAUTHORIZED)
        else:
            code = 401
            msg = ex.detail
    elif isinstance(ex,Http404):
        code = 400
        msg = "接口地址不正确"
    elif isinstance(ex, DRFAPIException):
        set_rollback()
        msg = ex.detail
        if isinstance(msg,dict):
            for k, v in msg.items():
                for i in v:
                    msg = "%s:%s" % (k, i)
    elif isinstance(ex, ProtectedError):
        set_rollback()
        msg = "删除失败:该条数据与其他数据有相关绑定"
    # elif isinstance(ex, DatabaseError):
    #     set_rollback()
    #     msg = "接口服务器异常,请联系管理员"
    elif isinstance(ex, Exception):
        logger.exception(traceback.format_exc())
        msg = str(ex)
    return ErrorResponse(msg=msg, code=code)