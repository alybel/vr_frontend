from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FormField, SelectField, FieldList
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class ConnectionSettingsForm(Form):
    own_twittername = StringField('twittername (e.g. @jondoe)')
    consumer_key = StringField('consumer_key', validators=[Required()])
    consumer_secret = StringField('consumer_secret', validators=[Required()])
    access_token = StringField('access_token', validators=[Required()])
    access_token_secret = StringField('access_token_secret', validators=[Required()])
    submit = SubmitField('Submit Information')

class AdvancedSettingsForm(Form):
    max_updates_per_day = IntegerField('maximum number updates per day')
    status_update_score = IntegerField('status update score')
    follow_score = IntegerField('follow score')
    retweet_score = IntegerField('retweet score')
    favorite_score = IntegerField('favorite score')
    number_active_favorites = IntegerField('number active favorites')
    number_active_retweets = IntegerField('number active retweets')
    number_active_follows = IntegerField('number active follows')
    only_with_url = BooleanField('only act on tweets with url')
    submit = SubmitField('Submit Information')

class KeywordForm(Form):
    keyword = StringField()
    weight = SelectField( choices = [('5', '5'),('7', '7'),('12','12')])
    submit = SubmitField('Add Item')

class BlacklistKeywordForm(Form):
    keyword = StringField()
    weight = SelectField( choices = [('-5', ' minus 5'),('-7', ' minus 7'),('-12','minus 12'), ('-1000', 'forbidden')])
    submit = SubmitField('Add Item')

