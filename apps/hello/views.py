from flask import views


def index():
    return 'Hello Word!'


def auth(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print("auth")
        return res

    return wrapper


def login(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print("login")
        return res


# 继承MethodView
class IndexView(views.MethodView):
    methods = ['GET', "POST"]  # 限制请求方式
    decorators = [auth, login]  # 添加装饰器,执行顺序自上而下

    def get(self, k1):
        print(k1)
        return 'GET 请求!'

    def post(self):
        return 'POST 请求!'
