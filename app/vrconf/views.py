from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user


from . import vrconf
from .. import db
from ..models import GeneralSettings
from ..email import send_email
from .forms import ConnectionSettingsForm

@vrconf.route('/connection_settings', methods=['GET', 'POST'])
def connection_settings():
    form = ConnectionSettingsForm()
    sett = GeneralSettings(
        email = current_user.email,
        consumer_key=form.consumer_key.data,
        consumer_secret=form.consumer_secret.data,
        access_token=form.access_token.data,
        access_token_secret = form.access_token_secret.data)
    db.session.add(sett)
    return render_template('vrconf/connection_settings.html', form=form)