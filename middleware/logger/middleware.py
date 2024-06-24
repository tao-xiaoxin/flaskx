import json

from flask import request, g
import time
import datetime
from loguru import logger


class LoggingMiddleware:
    def __init__(self, app=None, logger=logger):
        """
        初始化LoggingMiddleware中间件。
        :param app: Flask应用实例，如果提供，则立即初始化中间件。
        :param logger: 日志记录器实例。
        """
        self.logger = logger
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        将中间件的处理函数注册到Flask应用的请求处理流程中。
        :param app: Flask应用实例。
        """
        # 在请求开始前执行的函数
        app.before_request(self.before_request)
        # 在请求结束后执行的函数
        app.after_request(self.after_request)

    def before_request(self):
        """
        请求开始前执行的函数，用于记录请求的开始时间和基本信息。
        """
        g.log_info = dict()
        if 'X-Real-IP' in request.headers:
            g.remote_addr = request.headers['X-Real-IP']
        else:
            g.remote_addr = request.headers.get('X-Forwarded-For')
        if not g.remote_addr:
            g.remote_addr = request.remote_addr
        g.log_info['remote_addr'] = g.remote_addr
        g.log_info['request_json'] = request.get_json(silent=True)
        if not g.log_info['request_json']:
            g.log_info['request_data'] = request.data

        g.log_info['method'] = request.method
        g.log_info['url'] = request.url
        g.log_info['headers'] = dict(request.headers)
        g.log_info['start_time'] = time.time()
        g.now = int(time.time())
        g.now_m5 = g.now / 300 * 300
        # 记录请求开始的时间
        request.start_time = time.time()
        # 记录请求的方法和URL
        self.logger.info(f"Request started: {request.method} {request.url}")

    def after_request(self, response):
        """
        请求结束后执行的函数，用于记录请求的结束时间、处理时间、用户信息、状态码、响应头和响应内容。
        :param response: Flask响应对象。
        :return: 修改后的Flask响应对象。
        """
        # 记录请求结束的时间
        g.log_info['end_time'] = time.time()
        # 计算请求处理时间
        g.log_info['process_time'] = g.log_info['end_time'] - g.log_info['start_time']
        # 尝试获取用户信息
        g.log_info['user'] = g.get('user')
        # 记录响应状态码
        g.log_info['status_code'] = response.status_code
        # 更新响应头中的日期
        response.headers['Date'] = \
            (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        # 记录响应头
        g.log_info['ret_headers'] = dict(response.headers)
        # 如果响应内容是JSON，尝试解析并记录
        if response.content_type == 'application/json':
            g.log_info['ret'] = json.loads(response.data)

        # 根据响应状态码记录不同级别的日志
        if 400 <= response.status_code < 500:
            self.logger.warning(g.log_info)
        elif response.status_code >= 500:
            self.logger.error(g.log_info)
        else:
            self.logger.info(g.log_info)
        return response
