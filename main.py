import key
import tweepy
import os
from datetime import datetime

log_path = './trigger.log'


def trigger():
    # print('tofuchic_bot triggered')
    init_logfile(force=False)
    latest_datetime = get_latest_triggered_datetime()
    output_datetime_to_logfile()

    api = get_twitter_auth_api()
    n = 5
    # 最新n件のツイートを確認し、各機能にツイート情報を渡す
    for status in get_n_tweet(n, api):
        # print('status attributes : ' + str(dir(status)))
        # 最後にトリガされた時刻を使って重複チェックを排除
        if status.created_at < latest_datetime:
            break
        elif not hasattr(status, "retweeted_status"):
            # print('not RT')
            print(status.text)
            print(status.created_at)


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
    # Tweepy's process for setting up authorisation
    auth = tweepy.OAuthHandler(key.consumer_key, key.consumer_secret)
    auth.set_access_token(key.access_token, key.access_secret)
    return tweepy.API(auth)


def get_n_tweet(n, api):
    return tweepy.Cursor(api.home_timeline).items(n)


def tofufav():
    print('tofufav')
    return 0


if __name__ == '__main__':
    trigger()
    # init_logfile(force=False)
    # latest_datetime = get_latest_triggered_datetime()
    # output_datetime_to_logfile()
