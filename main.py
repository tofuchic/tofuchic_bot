import key
import tweepy


def trigger():
    print('tofuchic_bot triggered')
    for status in get_n_tweet(50):
        print(status.text)


def get_n_tweet(n):
    # Getting the key and secret codes from my environment variables
    consumer_key = key.consumer_key
    consumer_secret = key.consumer_secret
    access_token = key.access_token
    access_secret = key.access_secret

    # Tweepy's process for setting up authorisation
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    return tweepy.Cursor(api.home_timeline).items(n)


if __name__ == '__main__':
    trigger()
