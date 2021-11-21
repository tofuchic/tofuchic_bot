import key
import tweepy
import os
from datetime import datetime
import re
import random

log_path = './trigger.log'

n = 50

ng_words = ['@']
remove_ja_words = []
remove_en_words = ['tofubeat']
tofu_ja_words = ['豆腐', 'とうふ', 'トウフ', 'と－ふ', 'トーフ']
tofu_en_words = ['tofu', 'ｔｏｆｕ']
fav_ja_words = ['いいね', '良いね', 'ライク', 'ふぁぼ', 'ファボ']
fav_en_words = ['fav', 'like', 'ｆａｖ', 'ｌｉｋｅ']


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
    if (not os.path.exists('trigger.log')) | force:
        print('init log_file : ' + log_path)
        with open(log_path, mode='w') as log_file:
            log_file.write('')


def get_latest_triggered_datetime():
    with open(log_path) as log_file:
        # ログファイルの中身をリストとして取得
        log_lines = log_file.readlines()
        if log_lines != []:
            return datetime.strptime(log_lines[-1], '%Y-%m-%d %H:%M:%S\n')
        else:
            return datetime.strptime('2020-12-30 00:0:00', '%Y-%m-%d %H:%M:%S')


def output_datetime_to_logfile():
    with open(log_path) as log_file:
        # ログファイルの中身をリストとして取得
        log_lines = log_file.readlines()
    triggered_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + '\n'
    # ログファイルの末尾にトリガーされた時刻を追記
    log_lines.append(triggered_datetime)

    with open(log_path, mode='w') as log_file:
        log_file.writelines(log_lines)


def get_twitter_auth_api():
    # Tweepy's process for setting up authorization
    auth = tweepy.OAuthHandler(key.consumer_key, key.consumer_secret)
    auth.set_access_token(key.access_token, key.access_secret)
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

    ja_text = ''.join(re.findall('[一-龥ぁ-んァ-ヶ]+', status.text))
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


if __name__ == '__main__':
    trigger()
    # init_logfile(force=False)
    # latest_datetime = get_latest_triggered_datetime()
    # output_datetime_to_logfile()
