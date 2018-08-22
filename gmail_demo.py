#!/usr/bin/env python3
# coding:utf-8
from flask_mail import Message
from app import mail, app
msg = Message('test mail', sender='lesliebinbin19900129@gmail.com', recipients=['506120340@qq.com'])
msg.body = 'This is the plain text body'
msg.html = 'This is the <b>HTML</b> body'
with app.app_context():
    mail.send(msg)