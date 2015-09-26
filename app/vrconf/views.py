from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user


from . import vrconf
from .. import db
from ..models import GeneralSettings, WhiteList, BlackList,NeverUnfollowAccounts, User
from .forms import ConnectionSettingsForm, AdvancedSettingsForm, KeywordForm, BlacklistKeywordForm, NeverUnfollowForm, \
    OnOffForm

#ToDo write logic that users have a user_id that does not change when email changes
#ToDo write button with which connection to TWitter can be tested
#ToDo Write functionality to switch service on and off

@vrconf.route('/connection_settings', methods=['GET', 'POST'])
@login_required
def connection_settings():
    form = ConnectionSettingsForm()
    if form.validate_on_submit():
        sett = GeneralSettings.query.filter_by(fk_user_id=current_user.id).first()
        if sett is None:
            sett = GeneralSettings(
                fk_user_id = current_user.id,
                consumer_key=form.consumer_key.data,
                consumer_secret=form.consumer_secret.data,
                access_token=form.access_token.data,
                access_token_secret = form.access_token_secret.data,
                own_twittername=form.own_twittername.data.lstrip('@'))
            flash('Your Connection Settings have been stored')
            db.session.add(sett)
            return redirect(url_for('main.index'))
        else:
            sett.own_twittername = form.own_twittername.data
            sett.consumer_key = form.consumer_key.data
            sett.consumer_secret = form.consumer_secret.data
            sett.access_token = form.access_token.data
            sett.access_token_secret = form.access_token_secret.data
            #ToDo change the below line such that this is set true when connection settings are tested successfully
            current_user.connection_settings_set = True
            db.session.add(sett)
            db.session.commit()
            flash('Your Connection Settings have been changed')
            return redirect(url_for('main.index'))
    sett = GeneralSettings.query.filter_by(fk_user_id=current_user.id).first()
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
        sett = GeneralSettings.query.filter_by(fk_user_id=current_user.id).first()
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
    sett2 = GeneralSettings.query.filter_by(fk_user_id=current_user.id).first()
    if sett2 is None:
            flash('Please enter your settings information first')
            return redirect(url_for('vrconf.connection_settings'))
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
            fk_user_id=current_user.id,
            keyword=form.keyword.data,
            weight=form.weight.data)
        db.session.add(kwd)
        db.session.commit()
    kwds = WhiteList.query.filter_by(fk_user_id=current_user.id).all()
    return render_template('vrconf/target_settings.html', form=form, entries=kwds)

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
    kwds = WhiteList.query.filter_by(fk_user_id=current_user.id).all()
    return render_template('vrconf/target_settings.html', form2 = form2, entries=kwds)

@vrconf.route('/blacklist_settings', methods=['GET', 'POST'])
@login_required
def blacklist_settings():
    form = BlacklistKeywordForm()
    if form.validate_on_submit():
        kwd = BlackList(
            fk_user_id = current_user.id,
            keyword = form.keyword.data,
            weight = form.weight.data)
        db.session.add(kwd)
        db.session.commit()
    kwds = BlackList.query.filter_by(fk_user_id=current_user.id).all()
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
    kwds = BlackList.query.filter_by(fk_user_id=current_user.id).all()
    return render_template('vrconf/blacklist_settings.html', form2 = form, entries=kwds)


@vrconf.route('/never_unfollow_settings', methods=['GET', 'POST'])
@login_required
def never_unfollow_settings():
    form = NeverUnfollowForm()
    if form.validate_on_submit():
        account = NeverUnfollowAccounts(
            fk_user_id=current_user.id,
            accountname=form.account_name.data.lstrip('@')
        )
        db.session.add(account)
        db.session.commit()
    accounts = NeverUnfollowAccounts.query.filter_by(fk_user_id=current_user.id).all()
    return render_template('vrconf/account_never_unfollow_settings.html', form=form, entries=accounts)

@vrconf.route('/update_neverunfollow_entry', methods=['GET', 'POST'])
@login_required
def update_neverunfollow_entry():
    form = NeverUnfollowForm()
    del_id = request.form['id_to_delete']
    account_name = request.form['account_name']
    del_account = NeverUnfollowAccounts.query.filter_by(id=del_id).first()
    db.session.delete(del_account)
    db.session.commit()
    if 'change' in request.form:
        form.account_name.data = '@'+account_name
    accounts = NeverUnfollowAccounts.query.filter_by(fk_user_id=current_user.id).all()
    return render_template('vrconf/account_never_unfollow_settings.html', form=form, entries=accounts)


@vrconf.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    return render_template('vrconf/delete_account.html')

@vrconf.route('/yes_delete', methods=['GET', 'POST'])
@login_required
def yes_delete():
    flash('Your account has been deleted')
    accounts = NeverUnfollowAccounts.query.filter_by(fk_user_id=current_user.id).all()
    b_kwds = BlackList.query.filter_by(fk_user_id=current_user.id).all()
    w_kwds = WhiteList.query.filter_by(fk_user_id=current_user.id).all()
    sett = GeneralSettings.query.filter_by(fk_user_id=current_user.id).first()
    user =User.query.filter_by(id=current_user.id).first()
    for account in accounts:
        db.session.delete(account)
    for kwd in b_kwds:
        db.session.delete(kwd)
    for kwd in w_kwds:
        db.session.delete(kwd)
    if sett is not None:
        db.session.delete(sett)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('main.index'))

@vrconf.route('/onoff', methods=['GET', 'POST'])
@login_required
def onoff():
    form = OnOffForm()
    if form.validate_on_submit():
        sett = GeneralSettings.query.filter_by(fk_user_id=current_user.id).first()
        sett.onoff = 0 if sett.onoff == 1 else 1
        db.session.add(sett)
        db.session.commit()
    return redirect(url_for('main.index'))

