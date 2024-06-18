#!/usr/bin/env python
"""flask's command-line utility for administrative tasks."""
from application import create_app
def main():
    """Run administrative tasks."""
    app = create_app()

    # Run the application
    app.run()


if __name__ == '__main__':
    main()
