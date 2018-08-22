#!/usr/bin/env python3
# coding:utf-8
import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import Role, User

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """
    Run the unit tests.
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


def main():
    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == "__main__":
    main()
