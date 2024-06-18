from flask import Blueprint


def register_router(app, routers):
    """

    :param app:
    :param routers:
    :return:
    """
    for router_api in routers:
        if isinstance(router_api, Blueprint):
            app.register_blueprint(router_api)
        else:
            try:
                endpoint = router_api.__name__
                view_func = router_api.as_view(endpoint)
                # 如果没有服务名,默认 类名小写
                if hasattr(router_api, "service_name"):
                    url = '/{}/'.format(router_api.service_name.lower())
                else:
                    url = '/{}/'.format(router_api.__name__.lower())
                if 'GET' in router_api.__methods__:
                    app.add_url_rule(url, defaults={'key': None}, view_func=view_func, methods=['GET', ])
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['GET', ])
                if 'POST' in router_api.__methods__:
                    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
                if 'PUT' in router_api.__methods__:
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['PUT', ])
                if 'DELETE' in router_api.__methods__:
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['DELETE', ])
            except Exception as e:
                raise ValueError(e)


def init_bps(app):
    """
    注册蓝图
    :param app:
    :return:
    """
    # register_router()
    return app
