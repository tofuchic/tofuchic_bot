# Importing the libraries we'll use
import base64

import tweepy
import os
import random
from os import getenv
from datetime import datetime
import re

from google.cloud import firestore

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()
doc_ref = db.collection(u'tofuchic_bot').document(u'trigger_log')
doc = doc_ref.get()

n = 50

ng_words = ['@']
remove_ja_words = []
remove_en_words = ['tofubeat']
tofu_ja_words = ['豆腐', 'とうふ', 'トウフ', 'と－ふ', 'トーフ']
tofu_en_words = ['tofu', 'ｔｏｆｕ']
fav_ja_words = ['いいね', '良いね', 'ライク', 'ふぁぼ', 'ファボ']
fav_en_words = ['fav', 'like', 'ｆａｖ', 'ｌｉｋｅ']


def tofav(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
    else:
        name = 'World'
    print('Hello {}!'.format(name))

    trigger()


def trigger():
    # print('tofuchic_bot triggered')
    init_logfile(force=False)
    latest_datetime = get_latest_triggered_datetime()
    output_datetime_to_logfile()

    api = get_twitter_auth_api()
    # 最新n件のツイートを確認し、各機能にツイート情報を渡す
    for status in get_n_tweet(n, api):
        # [Tweepyのstatusリストで何が取れるのかわからなかったので、取り出してみた](https://qiita.com/Ryo87/items/61b5d54cbfd7ae520fe6)
        # print('status attributes : ' + str(dir(status)))

        # 最後にトリガされた時刻を使って重複チェックを排除
        # print(status.created_at, latest_datetime)
        if status.created_at < latest_datetime:
            break
        elif not hasattr(status, "retweeted_status"):
            tofufav(status, api)


def init_logfile(force=False):
    try:
        doc.to_dict()['triggered_datetime'][-1]
    except:
        doc_ref.set({
            u'triggered_datetime': ['2020-12-30 00:00:00']
        })

    if force:
        doc_ref.set({
            u'triggered_datetime': []
        })


def get_latest_triggered_datetime():
    print(u'get_latest_triggered_datetime : {}'.format(
        doc.to_dict()['triggered_datetime'][-1]))
    return datetime.strptime(doc.to_dict()['triggered_datetime'][-1], '%Y-%m-%d %H:%M:%S')


def output_datetime_to_logfile():
    doc_ref.update({u'triggered_datetime': firestore.ArrayUnion(
        [datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')])})


def get_twitter_auth_api():
    print('get_twitter_auth_api')
    # Getting the key and secret codes from my environment variables
    consumer_key = getenv("consumer_key")
    consumer_secret = getenv("consumer_secret")
    access_token = getenv("access_token")
    access_secret = getenv("access_secret")

    # Tweepy's process for setting up authorisation
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)


def get_n_tweet(n, api):
    return tweepy.Cursor(api.home_timeline).items(n)


def tofufav(status, api):
    # print('tofufav')

    # NGワードがあれば検査外
    for ng_word in ng_words:
        if ng_word in status.text:
            return 1

    tofu_flag = False
    fav_bomb_flag = False

    ja_text = ''.join(re.findall('[亜-熙ぁ-んァ-ヶ]+', status.text))
    for remove_ja_word in remove_ja_words:
        ja_text = ja_text.replace(remove_ja_word, '')
    en_text = ''.join(re.findall('[a-zａ-ｚ]+', status.text.lower()))
    for remove_en_word in remove_en_words:
        en_text = en_text.replace(remove_en_word, '')

    for tofu_ja_word in tofu_ja_words:
        if tofu_ja_word in ja_text:
            tofu_flag = True
            break
    for tofu_en_word in tofu_en_words:
        if tofu_en_word in en_text:
            tofu_flag = True
            break
    if tofu_flag:
        fav(status, api)
    else:
        return 1

    for fav_ja_word in fav_ja_words:
        if fav_ja_word in ja_text:
            fav_bomb_flag = True
            break
    for fav_en_word in fav_en_words:
        if fav_en_word in en_text:
            fav_bomb_flag = True
            break
    if fav_bomb_flag:
        fav_bomb(status, api)
    return 0


def fav(status, api):
    # print('fav')
    if not status.favorited:
        api.create_favorite(status.id)


def fav_bomb(tweet_status, api):
    # print('fav_bomb')
    fav_limit = random.randint(5, 10)
    fav_count = 0
    user_tweets = tweepy.Cursor(
        api.user_timeline, id=tweet_status.user.id).items(50)
    for user_status in user_tweets:
        # RTではない
        if not hasattr(user_status, "retweeted_status"):
            # NGワードが含まっている場合は無視
            ng_flag = False
            for ng_word in ng_words:
                if ng_word in user_status.text:
                    ng_flag = True
                    break
            if not ng_flag:
                fav(user_status, api)
                fav_count += 1
        if fav_count >= fav_limit:
            break
