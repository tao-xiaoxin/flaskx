from flask import Blueprint
from flask import views
from .views import index, IndexView

hello = Blueprint('hello', __name__)

hello.add_url_rule(rule='/', view_func=index, endpoint='index')


def init_blueprints(app):
    # CBV路由注册,as_view( )中必须传 name, name是该路由用于反向解析时的别名
    app.add_url_rule('/', view_func=IndexView.as_view(name='index2'),
                     defaults={'k1': 'hello word!'}, strict_slashes=False)
