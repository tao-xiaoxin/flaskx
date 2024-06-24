#!/usr/bin/env python
"""flask's command-line utility for administrative tasks."""
from flask import Flask
from application.factory import init_app


def create_app():
    """
    创建app
    :return:
    """
    app = Flask(__name__)
    init_app(app)

    return app


def main():
    """Run administrative tasks."""
    app = create_app()
    print(app.config)
    # Run the application
    app.run()


if __name__ == '__main__':
    main()
