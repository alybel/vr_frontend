from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user


from . import vrconf
from .. import db
from ..models import GeneralSettings, WhiteList, BlackList
from ..email import send_email
from .forms import ConnectionSettingsForm, AdvancedSettingsForm, KeywordForm, BlacklistKeywordForm


@vrconf.route('/connection_settings', methods=['GET', 'POST'])
@login_required
def connection_settings():
    form = ConnectionSettingsForm()
    if form.validate_on_submit():
        sett = GeneralSettings.query.filter_by(email=current_user.email).first()
        if sett is None:
            sett = GeneralSettings(
                email = current_user.email,
                consumer_key=form.consumer_key.data,
                consumer_secret=form.consumer_secret.data,
                access_token=form.access_token.data,
                access_token_secret = form.access_token_secret.data,
                own_twittername=form.own_twittername.data)
            flash('Your Connection Settings have been stored')
            db.session.add(sett)
            return redirect(url_for('main.index'))
        else:
            sett.own_twittername = form.own_twittername.data
            sett.consumer_key = form.consumer_key.data
            sett.consumer_secret = form.consumer_secret.data
            sett.access_token = form.access_token.data
            sett.access_token_secret = form.access_token_secret.data
            db.session.add(sett)
            db.session.commit()
            flash('Your Connection Settings have been changed')
            return redirect(url_for('main.index'))
    sett = GeneralSettings.query.filter_by(email=current_user.email).first()
    if not sett is None:
        form.own_twittername.data = sett.own_twittername
        form.access_token.data = sett.access_token
        form.access_token_secret.data = sett.access_token_secret
        form.consumer_key.data = sett.consumer_key
        form.consumer_secret.data = sett.consumer_secret
    return render_template('vrconf/connection_settings.html', form=form)

@vrconf.route('/advanced_settings', methods=['GET', 'POST'])
@login_required
def advanced_settings():
    form = AdvancedSettingsForm()
    if form.validate_on_submit():
        sett = GeneralSettings.query.filter_by(email=current_user.email).first()
        print sett.follow_score
        if sett is None:
            flash('Please enter your settings information first')
            return redirect(url_for('vrconf.connection_settings'))
        else:
            print 'DEBUG'
            print form.follow_score.data
            print 'DEBUG END'
            sett.max_updates_per_day = form.max_updates_per_day.data
            sett.status_update_score = form.status_update_score.data
            sett.follow_score = form.follow_score.data
            sett.retweet_score = form.retweet_score.data
            sett.favorite_score = form.favorite_score.data
            sett.only_with_url = form.only_with_url.data
            sett.number_active_follows = form.number_active_follows.data
            sett.number_active_retweets = form.number_active_retweets.data
            sett.number_active_favorites = form.number_active_favorites.data
            db.session.commit()
            flash('Your Advanced Settings have been stored')
            return redirect(url_for('main.index'))
    sett2 = GeneralSettings.query.filter_by(email=current_user.email).first()
    form.max_updates_per_day.data = sett2.max_updates_per_day
    form.only_with_url.data = sett2.only_with_url
    form.favorite_score.data = sett2.favorite_score
    form.follow_score.data = sett2.follow_score
    form.status_update_score.data = sett2.status_update_score
    form.number_active_favorites.data = sett2.number_active_favorites
    form.number_active_follows.data = sett2.number_active_follows
    form.number_active_retweets.data = sett2.number_active_retweets
    form.follow_score.data = sett2.follow_score
    form.retweet_score.data = sett2.retweet_score
    return render_template('vrconf/advanced_settings.html', form=form)

@vrconf.route('/target_settings', methods=['GET', 'POST'])
@login_required
def target_settings():
    form = KeywordForm()
    if form.validate_on_submit():
        kwd = WhiteList(
            email = current_user.email,
            keyword = form.keyword.data,
            weight = form.weight.data)
        db.session.add(kwd)
        db.session.commit()
    kwds = WhiteList.query.filter_by(email=current_user.email).all()
    return render_template('vrconf/target_settings.html', form2=form, entries=kwds)

@vrconf.route('/update_entry', methods=['GET', 'POST'])
@login_required
def update_entry():
    form2 = KeywordForm()
    del_id = request.form['id_to_delete']
    kwd = request.form['keyword']
    weight = request.form['weight']
    del_keyword = WhiteList.query.filter_by(id=del_id).first()
    db.session.delete(del_keyword)
    db.session.commit()
    if 'change' in request.form:
        form2.keyword.data = kwd
        form2.weight.data = weight
    kwds = WhiteList.query.filter_by(email=current_user.email).all()
    return render_template('vrconf/target_settings.html', form2 = form2, entries=kwds)

@vrconf.route('/blacklist_settings', methods=['GET', 'POST'])
@login_required
def blacklist_settings():
    form = BlacklistKeywordForm()
    if form.validate_on_submit():
        kwd = BlackList(
            email = current_user.email,
            keyword = form.keyword.data,
            weight = form.weight.data)
        db.session.add(kwd)
        db.session.commit()
    kwds = BlackList.query.filter_by(email=current_user.email).all()
    return render_template('vrconf/blacklist_settings.html', form2=form, entries=kwds)

@vrconf.route('/update_blacklist_entry', methods=['GET', 'POST'])
@login_required
def update_blacklist_entry():
    form = BlacklistKeywordForm()
    del_id = request.form['id_to_delete']
    kwd = request.form['keyword']
    weight = request.form['weight']
    del_keyword = BlackList.query.filter_by(id=del_id).first()
    db.session.delete(del_keyword)
    db.session.commit()
    if 'change' in request.form:
        form.keyword.data = kwd
        form.weight.data = weight
    kwds = BlackList.query.filter_by(email=current_user.email).all()
    return render_template('vrconf/blacklist_settings.html', form2 = form, entries=kwds)