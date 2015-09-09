from flask import render_template
from . import main
from ..vrconf.forms import OnOffForm
from ..models import GeneralSettings
from flask.ext.login import current_user

@main.route('/')
def index():
    sett = GeneralSettings.query.filter_by(fk_user_id=current_user.id).first()
    form = OnOffForm()
    form.submit.label.text = "switch off" if sett.onoff == 1 else "switch on"
    return render_template('index.html', form=form, onoff = sett.onoff)

