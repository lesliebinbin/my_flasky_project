from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db, mail
from ..models import User
from ..email import send_email
from flask import current_app


@main.route("/", methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if not user:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app._get_current_object().config['FLASKY_ADMIN']:
                send_email(
                    [current_app._get_current_object().config['FLASKY_ADMIN']],
                    'New user',
                    'mail/new_user',
                    user=user)
            else:
                send_email(
                    [
                        '506120340@qq.com',
                        'lesliebinbin19900129@gmail.com',
                    ],
                    'New user',
                    'mail/new_user',
                    user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template(
        "index.html",
        current_time=datetime.utcnow(),
        form=form,
        name=session.get('name'),
        known=session.get('known', False))