from app import create_app
import click
import os

app = create_app()


def create_app_structure(app_name):
    """创建应用结构的辅助函数"""
    app_structure = [
        f"{app_name}/__init__.py",
        f"{app_name}/models.py",
        f"{app_name}/views.py",
        f"{app_name}/tests.py",
        f"{app_name}/urls.py",
    ]
    for path in app_structure:
        if not path.endswith('/apps/'):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'a').close()


@app.cli.command("startapp")  # 注册命令
@click.argument("app_name")  # 命令参数
def startapp(app_name):
    """创建一个具有基本结构的新Flask应用。"""
    create_app_structure(app_name)
    click.echo(f"Flask app '{app_name}' created successfully.")


if __name__ == "__main__":
    app.run()
