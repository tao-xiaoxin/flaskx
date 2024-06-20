# -*- coding: utf-8 -*-

"""
@Remark: 自定义的Response文件
"""

from flask import Response, stream_with_context, jsonify


class SuccessResponse(Response):
    """
    标准响应成功的返回, SuccessResponse(data)或者SuccessResponse(data=data)
    (1)默认code返回2000, 不支持指定其他返回码
    """

    def __init__(self, data=None, code=2000, msg='success', status=None, headers=None, mimetype="application/json",
                 content_type=None, direct_passthrough=False, page=1, limit=1, total=1):
        """
        初始化成功响应对象。

        :param data: 实际返回的数据内容。
        :param msg: 响应消息，默认为'success'。
        :param status: HTTP状态码，默认为None，将使用Flask默认的状态码。
        :param headers: 附加到响应的HTTP头部，为字典或元组列表。
        :param mimetype: 响应的MIME类型，默认为'application/json'。
        :param content_type: 响应的内容类型，如果指定，将覆盖mimetype参数。
        :param direct_passthrough: 是否直接传递响应而不进行任何处理，默认为False。
        :param page: 分页中的当前页码，默认为1。
        :param limit: 分页中每页的项目数，默认为1。
        :param total: 分页中的总项目数，默认为1。
        """
        if not data:
            total = 0
        response = {
            "code": code,
            "data": {
                "page": page,
                "limit": limit,
                "total": total,
                "data": data
            },
            "msg": msg
        }
        super().__init__(response=response, status=status, headers=headers, mimetype=mimetype,
                         content_type=content_type, direct_passthrough=direct_passthrough)


class DetailResponse(Response):
    """
    不包含分页信息的接口返回,主要用于单条数据查询
    (1)默认code返回2000, 不支持指定其他返回码
    """

    def __init__(self, data=None, code=2000, msg='success', status=None, headers=None, mimetype="application/json",
                 content_type=None, direct_passthrough=False):
        response = {
            "code": code,
            "data": data,
            "msg": msg
        }
        super().__init__(response=response, status=status, headers=headers, mimetype=mimetype,
                         content_type=content_type, direct_passthrough=direct_passthrough)


class ErrorResponse(Response):
    """
    标准响应错误的返回,ErrorResponse(msg='xxx')
    (1)默认错误码返回400, 也可以指定其他返回码:ErrorResponse(code=xxx)
    """

    def __init__(self, data=None, code=400, msg='error', status=None, headers=None, mimetype="application/json",
                 content_type=None, direct_passthrough=False):
        response = {
            "code": code,
            "data": data,
            "msg": msg
        }
        super().__init__(response=response, status=status, headers=headers, mimetype=mimetype,
                         content_type=content_type, direct_passthrough=direct_passthrough)


class StreamResponse(Response):
    """
    专门用于流式输出的成功响应类。
    StreamResponse(yield_function, args，kwargs)或者StreamResponse(yield_function=yield_function, args=args，kwargs=kwargs)
    默认headers包含适用于流式输出的设置。
    """

    def __init__(self, yield_function, args, kwargs, status=None, headers=None, mimetype="text/event-stream",
                 content_type=None, direct_passthrough=False, ):
        # 定义默认的流式输出响应头
        default_headers = {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
        }
        # 如果提供了额外的headers，则更新默认headers
        if headers:
            default_headers.update(headers)

        # 使用stream_with_context包装yield_function
        data = stream_with_context(yield_function(*args, **kwargs))

        # 调用父类构造函数
        super().__init__(response=data, status=status, headers=headers, mimetype=mimetype,
                         content_type=content_type, direct_passthrough=direct_passthrough)


def success_data(data, code=200, msg='success'):
    """
    通用响应体函数，流式输出的成功响应体。
    :param data: 实际返回的数据内容。
    :param code: 响应码，默认为200。
    :param msg: 响应消息，默认为'success'。
    :return: 一个响应体。
    """
    res = {
        "code": code,
        "data": data,
        "msg": msg
    }
    return res


def error_data(data, code=400, msg='error'):
    """
    通用错误体响应函数，流式输出的错误响应体。
    :param data: 实际返回的数据内容。
    :param code: 响应码，默认为400。
    :param msg: 响应消息，默认为'error'。
    :return: 一个错误响应体。
    """
    res = {
        "code": code,
        "data": data,
        "msg": msg
    }
    return res
