from flask import Blueprint

hello = Blueprint('hello', __name__)





hello.add_url_rule(rule='/', view_func=index, endpoint='index')
