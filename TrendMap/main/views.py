from django.shortcuts import render, redirect

import tweepy
import json
# Create your views here.

def index(request):
    context= {}
    return render(request, 'index.html', context)


def begin_twitter_authentication(request):
    """ Read the secrets file and build the auth object """
    with open('../certs/client_secrets.json') as f:
        data = json.load(f)
    consumer_key = data.secrets.APIkey
    consumer_secret = data.secrets.APIkeySecret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    request.session['request_token'] = auth.request_token
    return redirect(redirect_url)

def finish_twitter_authentication(request):
    """ Get the verifier """
    verifier = request.GET.get('oauth_verifier')

    """ Open the secrets file and rebuild the auth object """
    with open('../certs/client_secrets.json') as f:
        data = json.load(f)
    consumer_key = data.secrets.APIkey
    consumer_secret = data.secrets.APIkeySecret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    token = request.session['request_token']
    del request.session['request_token']
    auth.request_token = {
        'oauth_token': token,
        'oauth_token_secret': verifier
    }

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    """ Remember to save these values in order to use them later """
    Tokens.objects.create(key = auth.access_token,secret = auth.access_token_secret)


    return redirect('/')



def get_tweets(request):
    """ Open the secrets file and rebuild the auth object """
    token = Tokens.objects.get(id=1)
    auth.set_access_token(token.key, token.secret)


    api = tweepy.API(auth)
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
    context= {
        'public_tweets': public_tweets,
    }
    return render(request, 'index.html', context)
