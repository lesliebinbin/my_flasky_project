from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from . import main
from .forms import NameForm, EditProfileForm
from .. import db, mail
from ..models import User
from ..email import send_email
from flask import current_app
from threading import Thread
from flask_login import current_user


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


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)