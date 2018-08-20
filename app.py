#!/usr/bin/env python3
# coding:utf-8
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
app = Flask(__name__)
bootstrap = Bootstrap(app=app)
moment = Moment(app=app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/user/<name>')
def user(name):
    age = request.args.get("age")
    return render_template('user.html', name=name, age=age)


@app.route('/inheritance')
def inheritance():
    return render_template('inheritance.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
