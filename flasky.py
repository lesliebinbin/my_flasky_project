#!/usr/bin/env python3
# coding:utf-8
import os, sys, click

from flask_migrate import Migrate

from app import create_app, db
from app.models import Role, User, Permission
from flask_migrate import upgrade

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))
migrate = Migrate(app, db)

COV = None
if os.environ.get('FLASKY_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)


@app.cli.command()
@click.option(
    '--coverage/--no-coverage',
    default=False,
    help='Run tests under code coverage.')
def test(coverage):
    """
    Run the unit tests.
    """
    if coverage and not os.environ.get('FLASKY_COVERAGE'):
        os.environ['FLASKY_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print("HTML version: file://{}/index.html".format(covdir))
        COV.erase()


@app.cli.command()
def deploy():
    upgrade()
    Role.insert_roles()


def main():
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    main()
