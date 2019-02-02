from django.shortcuts import render, redirect

import tweepy


# Create your views here.

def index(request):
    context= {}
    return render(request, 'index.html', context)


def get_tweets(request):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
    context= {
        'public_tweets': public_tweets,
    }
    return render(request, 'index.html', context)
